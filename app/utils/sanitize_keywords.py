"""Keyword sanitization utilities."""

import logging
import re
from typing import List

logger = logging.getLogger(__name__)


def sanitize_keywords(keywords: List[str]) -> List[str]:
    """
    Sanitize and normalize keywords.

    Args:
        keywords: List of keyword strings

    Returns:
        Sanitized keywords list
    """
    sanitized = []
    for keyword in keywords:
        # Trim whitespace
        keyword = keyword.strip()

        # Remove excessive whitespace
        keyword = re.sub(r"\s+", " ", keyword)

        # Keep only alphanumeric, spaces, and common punctuation
        keyword = re.sub(r"[^\w\s-]", "", keyword)

        # Remove if empty after sanitization
        if keyword:
            sanitized.append(keyword)

    logger.debug(f"Sanitized {len(keywords)} keywords to {len(sanitized)}")
    return sanitized





