from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Resume:
    """Represents a candidate resume."""
    id: str
    candidate_name: str
    raw_text: str
    filename: Optional[str] = None
    score: float = 0.0
    matched_keywords: list = field(default_factory=list)
    rank: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "candidate_name": self.candidate_name,
            "filename": self.filename,
            "score": round(self.score * 100, 2),
            "matched_keywords": self.matched_keywords,
            "rank": self.rank,
            "preview": self.raw_text[:300] + "..." if len(self.raw_text) > 300 else self.raw_text,
        }


@dataclass
class JobDescription:
    """Represents a job description."""
    title: str
    raw_text: str
    required_skills: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "required_skills": self.required_skills,
            "preview": self.raw_text[:300] + "..." if len(self.raw_text) > 300 else self.raw_text,
        }