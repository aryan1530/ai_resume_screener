from flask import Blueprint, request, jsonify

from app.models.resume_model import Resume, JobDescription
from app.services.scoring_service import ScoringService
from app.utils.file_parser import FileParser

resume_bp = Blueprint("resume", __name__)
_scoring_service = ScoringService()
_file_parser = FileParser()


@resume_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "AI Resume Screener API is running"})


@resume_bp.route("/screen", methods=["POST"])
def screen_resumes():
    """
    POST /api/screen
    Form data:
      - job_title       (str)
      - job_description (str)
      - resumes[]       (files: pdf or txt)
    """
    # --- Validate inputs ---
    job_title = request.form.get("job_title", "").strip()
    job_description_text = request.form.get("job_description", "").strip()
    files = request.files.getlist("resumes")

    errors = []
    if not job_title:
        errors.append("job_title is required.")
    if not job_description_text:
        errors.append("job_description is required.")
    if not files or all(f.filename == "" for f in files):
        errors.append("At least one resume file is required.")
    if errors:
        return jsonify({"error": " | ".join(errors)}), 400

    # --- Build JobDescription ---
    job = JobDescription(title=job_title, raw_text=job_description_text)

    # --- Parse resume files ---
    resumes = []
    parse_errors = []
    for file in files:
        if file.filename == "":
            continue
        if not FileParser.allowed_file(file.filename):
            parse_errors.append(f"{file.filename}: unsupported format (use PDF or TXT).")
            continue
        try:
            raw_bytes = file.read()
            text, candidate_name = FileParser.parse(raw_bytes, file.filename)
            if not text:
                parse_errors.append(f"{file.filename}: could not extract text.")
                continue
            resumes.append(
                Resume(
                    id=FileParser.generate_id(),
                    candidate_name=candidate_name,
                    raw_text=text,
                    filename=file.filename,
                )
            )
        except Exception as exc:
            parse_errors.append(f"{file.filename}: {str(exc)}")

    if not resumes:
        return jsonify({"error": "No valid resumes could be parsed.", "details": parse_errors}), 422

    # --- Score & rank ---
    ranked_resumes = _scoring_service.score_resumes(job, resumes)
    stats = _scoring_service.get_score_distribution(ranked_resumes)

    return jsonify(
        {
            "job": job.to_dict(),
            "results": [r.to_dict() for r in ranked_resumes],
            "stats": stats,
            "parse_warnings": parse_errors,
            "total_screened": len(ranked_resumes),
        }
    )


@resume_bp.route("/sample-jd", methods=["GET"])
def sample_jd():
    """Returns a sample job description for quick testing."""
    return jsonify(
        {
            "title": "Senior Python Developer",
            "description": (
                "We are looking for a Senior Python Developer with 4+ years of experience. "
                "Required skills: Python, Django or Flask, REST APIs, PostgreSQL, Redis, Docker, "
                "Kubernetes, AWS or GCP, Git. Experience with machine learning libraries such as "
                "scikit-learn, pandas, numpy is a strong plus. Knowledge of CI/CD pipelines, "
                "agile methodologies, and test-driven development is expected. "
                "Excellent communication and problem-solving skills required."
            ),
        }
    )