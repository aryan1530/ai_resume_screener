from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.resume_model import Resume, JobDescription
from app.services.nlp_service import NLPPreprocessor


class ScoringService:
    """
    Ranks resumes against a job description using TF-IDF + cosine similarity.
    Follows Single Responsibility Principle — only concerned with scoring.
    """

    def __init__(self):
        self._preprocessor = NLPPreprocessor()
        self._vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),   # unigrams + bigrams for better phrase matching
            max_features=5000,
            sublinear_tf=True,    # log normalization
        )

    def _preprocess_corpus(self, texts: List[str]) -> List[str]:
        return [self._preprocessor.preprocess(t) for t in texts]

    def score_resumes(
        self, job: JobDescription, resumes: List[Resume]
    ) -> List[Resume]:
        """
        Compute TF-IDF cosine similarity of each resume vs the job description.
        Returns resumes sorted by descending score with rank assigned.
        """
        if not resumes:
            return []

        corpus = [job.raw_text] + [r.raw_text for r in resumes]
        processed = self._preprocess_corpus(corpus)

        try:
            tfidf_matrix = self._vectorizer.fit_transform(processed)
        except ValueError:
            # Edge case: all documents are empty after preprocessing
            for resume in resumes:
                resume.score = 0.0
            return resumes

        jd_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]

        scores: np.ndarray = cosine_similarity(jd_vector, resume_vectors).flatten()

        jd_keywords = set(self._preprocessor.extract_keywords(job.raw_text, top_n=20))

        for idx, resume in enumerate(resumes):
            resume.score = float(scores[idx])
            resume_keywords = set(
                self._preprocessor.extract_keywords(resume.raw_text, top_n=30)
            )
            resume.matched_keywords = sorted(jd_keywords & resume_keywords)

        ranked = sorted(resumes, key=lambda r: r.score, reverse=True)
        for rank, resume in enumerate(ranked, start=1):
            resume.rank = rank

        return ranked

    def get_score_distribution(self, resumes: List[Resume]) -> dict:
        """Return summary statistics for UI display."""
        if not resumes:
            return {}
        scores = [r.score * 100 for r in resumes]
        return {
            "mean": round(float(np.mean(scores)), 2),
            "max": round(float(np.max(scores)), 2),
            "min": round(float(np.min(scores)), 2),
            "std": round(float(np.std(scores)), 2),
        }