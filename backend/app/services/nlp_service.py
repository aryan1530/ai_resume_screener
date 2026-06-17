import re
import string
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data on first import
for resource in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]:
    nltk.download(resource, quiet=True)


class NLPPreprocessor:
    """Handles text cleaning, tokenization, and lemmatization using OOP design."""

    def __init__(self):
        self._lemmatizer = WordNetLemmatizer()
        self._stop_words = set(stopwords.words("english"))
        # Keep important tech/resume keywords
        self._stop_words -= {"not", "no", "nor", "more", "most", "above", "below"}

    def clean_text(self, text: str) -> str:
        """Remove noise from raw text."""
        text = text.lower()
        text = re.sub(r"http\S+|www\S+", "", text)          # URLs
        text = re.sub(r"\S+@\S+", "", text)                  # emails
        text = re.sub(r"\d+", " ", text)                     # numbers
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> List[str]:
        """Tokenize and remove stopwords."""
        tokens = word_tokenize(text)
        return [t for t in tokens if t not in self._stop_words and len(t) > 2]

    def lemmatize(self, tokens: List[str]) -> List[str]:
        """Reduce tokens to base form."""
        return [self._lemmatizer.lemmatize(token) for token in tokens]

    def preprocess(self, text: str) -> str:
        """Full pipeline: clean → tokenize → lemmatize → rejoin."""
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        lemmatized = self.lemmatize(tokens)
        return " ".join(lemmatized)

    def extract_keywords(self, text: str, top_n: int = 15) -> List[str]:
        """Extract the most frequent meaningful keywords."""
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        lemmatized = self.lemmatize(tokens)
        freq: dict = {}
        for token in lemmatized:
            freq[token] = freq.get(token, 0) + 1
        sorted_words = sorted(freq, key=freq.get, reverse=True)
        return sorted_words[:top_n]