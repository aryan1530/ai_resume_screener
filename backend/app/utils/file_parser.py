import io
import uuid
from typing import Tuple

import PyPDF2


class FileParser:
    """Parses uploaded resume files into plain text."""

    ALLOWED_EXTENSIONS = {"pdf", "txt"}

    @staticmethod
    def allowed_file(filename: str) -> bool:
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in FileParser.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def parse(file_bytes: bytes, filename: str) -> Tuple[str, str]:
        """
        Returns (extracted_text, candidate_name).
        Candidate name is inferred from the filename.
        """
        ext = filename.rsplit(".", 1)[1].lower()
        candidate_name = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()

        if ext == "pdf":
            text = FileParser._parse_pdf(file_bytes)
        else:
            text = file_bytes.decode("utf-8", errors="replace")

        return text.strip(), candidate_name

    @staticmethod
    def _parse_pdf(file_bytes: bytes) -> str:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text)
        return "\n".join(pages)

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())[:8]