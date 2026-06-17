"""
Unit tests for the AI Resume Screener.
Run with: pytest tests/ -v
"""
import pytest

from app.models.resume_model import Resume, JobDescription
from app.services.nlp_service import NLPPreprocessor
from app.services.scoring_service import ScoringService
from app.utils.file_parser import FileParser


# ────────────────────────────────────────────────
# Fixtures
# ────────────────────────────────────────────────

@pytest.fixture
def preprocessor():
    return NLPPreprocessor()


@pytest.fixture
def scoring_service():
    return ScoringService()


@pytest.fixture
def sample_job():
    return JobDescription(
        title="Python Developer",
        raw_text=(
            "Looking for a Python developer with experience in Django, REST APIs, "
            "PostgreSQL, Docker, and machine learning using scikit-learn and pandas."
        ),
    )


@pytest.fixture
def strong_resume():
    return Resume(
        id="r001",
        candidate_name="Alice Smith",
        raw_text=(
            "Experienced Python developer with 5 years working on Django REST APIs. "
            "Strong background in PostgreSQL database design, Docker containerization, "
            "and machine learning with scikit-learn, pandas, and numpy."
        ),
    )


@pytest.fixture
def weak_resume():
    return Resume(
        id="r002",
        candidate_name="Bob Jones",
        raw_text=(
            "Java developer with experience in Spring Boot and Oracle databases. "
            "Worked on Android mobile applications and UI design."
        ),
    )


# ────────────────────────────────────────────────
# NLPPreprocessor tests
# ────────────────────────────────────────────────

class TestNLPPreprocessor:

    def test_clean_text_lowercases(self, preprocessor):
        result = preprocessor.clean_text("Hello WORLD")
        assert result == "hello world"

    def test_clean_text_removes_urls(self, preprocessor):
        result = preprocessor.clean_text("Visit https://example.com for info")
        assert "http" not in result
        assert "example" not in result

    def test_clean_text_removes_email(self, preprocessor):
        result = preprocessor.clean_text("Contact me at user@domain.com")
        assert "@" not in result

    def test_clean_text_removes_numbers(self, preprocessor):
        result = preprocessor.clean_text("5 years experience, 3 projects")
        assert not any(c.isdigit() for c in result)

    def test_tokenize_removes_stopwords(self, preprocessor):
        tokens = preprocessor.tokenize("this is a test of the system")
        assert "is" not in tokens
        assert "the" not in tokens
        assert "a" not in tokens

    def test_tokenize_removes_short_tokens(self, preprocessor):
        tokens = preprocessor.tokenize("python api db")
        assert "db" not in tokens   # length 2

    def test_lemmatize_returns_base_form(self, preprocessor):
        tokens = ["running", "developers", "worked"]
        result = preprocessor.lemmatize(tokens)
        assert "running" in result or "run" in result

    def test_preprocess_returns_string(self, preprocessor):
        result = preprocessor.preprocess("Experienced Python Developer with 5 years")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_preprocess_empty_string(self, preprocessor):
        result = preprocessor.preprocess("")
        assert result == ""

    def test_extract_keywords_returns_list(self, preprocessor):
        text = "python django flask rest api python django python"
        keywords = preprocessor.extract_keywords(text, top_n=3)
        assert isinstance(keywords, list)
        assert len(keywords) <= 3
        assert keywords[0] == "python"

    def test_extract_keywords_top_n_limit(self, preprocessor):
        text = "python django flask rest api docker kubernetes aws gcp redis"
        keywords = preprocessor.extract_keywords(text, top_n=5)
        assert len(keywords) <= 5


# ────────────────────────────────────────────────
# ScoringService tests
# ────────────────────────────────────────────────

class TestScoringService:

    def test_strong_resume_scores_higher(self, scoring_service, sample_job, strong_resume, weak_resume):
        results = scoring_service.score_resumes(sample_job, [strong_resume, weak_resume])
        strong = next(r for r in results if r.id == "r001")
        weak = next(r for r in results if r.id == "r002")
        assert strong.score > weak.score

    def test_scores_between_zero_and_one(self, scoring_service, sample_job, strong_resume, weak_resume):
        results = scoring_service.score_resumes(sample_job, [strong_resume, weak_resume])
        for r in results:
            assert 0.0 <= r.score <= 1.0

    def test_rank_assigned_correctly(self, scoring_service, sample_job, strong_resume, weak_resume):
        results = scoring_service.score_resumes(sample_job, [weak_resume, strong_resume])
        rank1 = next(r for r in results if r.rank == 1)
        rank2 = next(r for r in results if r.rank == 2)
        assert rank1.score >= rank2.score

    def test_empty_resumes_returns_empty(self, scoring_service, sample_job):
        results = scoring_service.score_resumes(sample_job, [])
        assert results == []

    def test_matched_keywords_are_list(self, scoring_service, sample_job, strong_resume):
        results = scoring_service.score_resumes(sample_job, [strong_resume])
        assert isinstance(results[0].matched_keywords, list)

    def test_single_resume_ranks_one(self, scoring_service, sample_job, strong_resume):
        results = scoring_service.score_resumes(sample_job, [strong_resume])
        assert results[0].rank == 1

    def test_score_distribution_keys(self, scoring_service, sample_job, strong_resume, weak_resume):
        results = scoring_service.score_resumes(sample_job, [strong_resume, weak_resume])
        dist = scoring_service.get_score_distribution(results)
        assert "mean" in dist
        assert "max" in dist
        assert "min" in dist
        assert "std" in dist

    def test_score_distribution_empty(self, scoring_service):
        dist = scoring_service.get_score_distribution([])
        assert dist == {}

    def test_identical_resumes_same_score(self, scoring_service, sample_job):
        r1 = Resume(id="a", candidate_name="A", raw_text="Python Django REST API PostgreSQL Docker")
        r2 = Resume(id="b", candidate_name="B", raw_text="Python Django REST API PostgreSQL Docker")
        results = scoring_service.score_resumes(sample_job, [r1, r2])
        assert abs(results[0].score - results[1].score) < 1e-6


# ────────────────────────────────────────────────
# FileParser tests
# ────────────────────────────────────────────────

class TestFileParser:

    def test_allowed_file_pdf(self):
        assert FileParser.allowed_file("resume.pdf") is True

    def test_allowed_file_txt(self):
        assert FileParser.allowed_file("resume.txt") is True

    def test_allowed_file_docx_rejected(self):
        assert FileParser.allowed_file("resume.docx") is False

    def test_allowed_file_no_extension(self):
        assert FileParser.allowed_file("resume") is False

    def test_parse_txt_returns_text(self):
        content = b"Experienced Python Developer with Flask and Django."
        text, name = FileParser.parse(content, "john_doe.txt")
        assert "Python" in text
        assert name == "John Doe"

    def test_candidate_name_from_filename(self):
        _, name = FileParser.parse(b"some text", "alice_smith.txt")
        assert name == "Alice Smith"

    def test_generate_id_is_string(self):
        uid = FileParser.generate_id()
        assert isinstance(uid, str)
        assert len(uid) == 8


# ────────────────────────────────────────────────
# Resume model tests
# ────────────────────────────────────────────────

class TestResumeModel:

    def test_to_dict_contains_required_keys(self):
        r = Resume(id="x1", candidate_name="Test User", raw_text="Python developer")
        d = r.to_dict()
        for key in ["id", "candidate_name", "score", "matched_keywords", "rank", "preview"]:
            assert key in d

    def test_score_converted_to_percentage(self):
        r = Resume(id="x1", candidate_name="Test", raw_text="text", score=0.75)
        assert r.to_dict()["score"] == 75.0

    def test_preview_truncated_for_long_text(self):
        long_text = "a" * 400
        r = Resume(id="x1", candidate_name="Test", raw_text=long_text)
        assert r.to_dict()["preview"].endswith("...")

    def test_preview_not_truncated_for_short_text(self):
        short_text = "Short resume"
        r = Resume(id="x1", candidate_name="Test", raw_text=short_text)
        assert not r.to_dict()["preview"].endswith("...")