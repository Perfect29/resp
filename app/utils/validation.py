"""Input validation utilities."""

import re
from typing import List
from urllib.parse import urlparse

import logging

logger = logging.getLogger(__name__)


def validate_url(url: str) -> str:
    """
    Validate that URL is a public http/https URL.

    Args:
        url: URL string to validate

    Returns:
        Normalized URL string

    Raises:
        ValueError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    url = url.strip()

    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValueError(f"Invalid URL format: {e}") from e

    # Check scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https protocol")

    # Check netloc
    if not parsed.netloc:
        raise ValueError("URL must have a valid domain")

    # Reconstruct normalized URL
    normalized = f"{parsed.scheme}://{parsed.netloc}"
    if parsed.path:
        normalized += parsed.path
    if parsed.query:
        normalized += f"?{parsed.query}"
    if parsed.fragment:
        normalized += f"#{parsed.fragment}"

    return normalized


def validate_keywords(keywords: List[str]) -> List[str]:
    """
    Validate keywords list.

    Args:
        keywords: List of keyword strings

    Returns:
        Validated and sanitized keywords list

    Raises:
        ValueError: If validation fails
    """
    if not isinstance(keywords, list):
        raise ValueError("Keywords must be a list")

    if len(keywords) > 5:
        raise ValueError("Maximum 5 keywords allowed")

    if len(keywords) < 1:
        raise ValueError("At least 1 keyword required")

    validated = []
    for keyword in keywords:
        if not isinstance(keyword, str):
            raise ValueError("All keywords must be strings")

        keyword = keyword.strip()

        if not keyword:
            raise ValueError("Keywords cannot be empty")

        if len(keyword) < 2 or len(keyword) > 40:
            raise ValueError("Each keyword must be between 2 and 40 characters")

        validated.append(keyword)

    return validated


def validate_prompts(prompts: List[str]) -> List[str]:
    """
    Validate prompts list.

    Args:
        prompts: List of prompt strings

    Returns:
        Validated and sanitized prompts list

    Raises:
        ValueError: If validation fails
    """
    if not isinstance(prompts, list):
        raise ValueError("Prompts must be a list")

    if len(prompts) > 5:
        raise ValueError("Maximum 5 prompts allowed")

    if len(prompts) < 1:
        raise ValueError("At least 1 prompt required")

    # Check for internal URLs in prompts
    url_pattern = re.compile(
        r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+)",
        re.IGNORECASE,
    )

    validated = []
    for prompt in prompts:
        if not isinstance(prompt, str):
            raise ValueError("All prompts must be strings")

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompts cannot be empty")

        if len(prompt) > 200:
            raise ValueError("Each prompt must be 200 characters or less")

        # Check for internal URLs
        if url_pattern.search(prompt):
            raise ValueError("Prompts cannot contain internal/localhost URLs")

        validated.append(prompt)

    return validated


def validate_business_name(name: str) -> str:
    """
    Validate business name.

    Args:
        name: Business name string

    Returns:
        Validated and sanitized business name

    Raises:
        ValueError: If validation fails
    """
    if not name or not isinstance(name, str):
        raise ValueError("Business name must be a non-empty string")

    name = name.strip()

    if not name:
        raise ValueError("Business name cannot be empty or whitespace only")

    if len(name) < 2 or len(name) > 80:
        raise ValueError("Business name must be between 2 and 80 characters")

    return name





