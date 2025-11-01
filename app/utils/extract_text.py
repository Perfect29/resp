"""Text extraction utilities from HTML content."""

import logging
from typing import List

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract_text_from_html(html: str) -> str:
    """
    Extract readable text content from HTML.

    Args:
        html: HTML content string

    Returns:
        Extracted text content
    """
    try:
        soup = BeautifulSoup(html, "lxml")

        # Remove script and style elements
        for script in soup(["script", "style", "noscript"]):
            script.decompose()

        # Get text and clean up whitespace
        text = soup.get_text(separator=" ", strip=True)

        # Clean up multiple whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)

        logger.debug(f"Extracted {len(text)} characters of text")
        return text

    except Exception as e:
        logger.error(f"Error extracting text from HTML: {e}")
        raise ValueError(f"Failed to extract text from HTML: {e}") from e


def extract_meta_keywords(html: str) -> List[str]:
    """
    Extract keywords from HTML meta tags.

    Args:
        html: HTML content string

    Returns:
        List of keywords from meta tags
    """
    try:
        soup = BeautifulSoup(html, "lxml")

        keywords = []

        # Check meta keywords tag
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        if meta_keywords and meta_keywords.get("content"):
            content = meta_keywords.get("content", "")
            keywords.extend([kw.strip() for kw in content.split(",") if kw.strip()])

        # Meta description available but not used for keyword extraction currently
        # (placeholder for future enhancement)

        logger.debug(f"Extracted {len(keywords)} keywords from meta tags")
        return keywords

    except Exception as e:
        logger.error(f"Error extracting meta keywords: {e}")
        return []

