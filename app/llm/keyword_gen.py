"""Keyword generation from text content with OpenAI integration."""

import hashlib
import logging
import re
from typing import List

from app.config import settings

logger = logging.getLogger(__name__)

# Try to import OpenAI, but allow graceful degradation if not available
try:
    from openai import AsyncOpenAI

    openai_available = True
except ImportError:
    openai_available = False
    logger.warning("OpenAI library not installed. Using stub implementation.")


async def generate_keywords(text: str, count: int = 5) -> List[str]:
    """
    Generate suggested keywords from text content.

    Uses OpenAI API if API key is configured, otherwise falls back to
    heuristic-based extraction.

    Args:
        text: Text content to analyze
        count: Number of keywords to generate (default: 5)

    Returns:
        List of suggested keywords
    """
    logger.info(f"Generating {count} keywords from text (length: {len(text)})")

    # Use OpenAI if API key is available
    if (
        openai_available
        and settings.openai_api_key
        and settings.openai_api_key.strip()
    ):
        try:
            return await _generate_keywords_with_openai(text, count)
        except Exception as e:
            logger.warning(f"OpenAI keyword generation failed: {e}, falling back to stub")
            # Fall through to stub implementation

    # Fallback to heuristic-based extraction

    # Extract words (alphanumeric sequences)
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())

    # Simple frequency counting
    word_freq: dict[str, int] = {}
    for word in words:
        # Filter out common stop words
        stop_words = {
            "the",
            "and",
            "for",
            "are",
            "but",
            "not",
            "you",
            "all",
            "can",
            "her",
            "was",
            "one",
            "our",
            "out",
            "day",
            "get",
            "has",
            "him",
            "his",
            "how",
            "its",
            "may",
            "new",
            "now",
            "old",
            "see",
            "two",
            "way",
            "who",
            "boy",
            "did",
            "its",
            "let",
            "put",
            "say",
            "she",
            "too",
            "use",
        }
        if word not in stop_words and len(word) >= 3:
            word_freq[word] = word_freq.get(word, 0) + 1

    # Sort by frequency and get top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Take top keywords, but ensure variety
    keywords: List[str] = []
    seen = set()

    for word, _freq in sorted_words[:count * 2]:  # Get more candidates
        if word not in seen and len(keywords) < count:
            keywords.append(word.capitalize())
            seen.add(word)

    # If we don't have enough, pad with generic ones
    while len(keywords) < count:
        # Use deterministic hash-based generation for consistency
        hash_input = f"{text}_{len(keywords)}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()
        generic_keyword = f"Keyword{len(keywords) + 1}"
        keywords.append(generic_keyword)

    logger.info(f"Generated keywords: {keywords}")
    return keywords[:count]


async def _generate_keywords_with_openai(text: str, count: int) -> List[str]:
    """
    Generate keywords using OpenAI API.

    Args:
        text: Text content to analyze
        count: Number of keywords to generate

    Returns:
        List of suggested keywords
    """
    if not openai_available:
        raise ImportError("OpenAI library not available")

    client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=settings.openai_timeout)

    # Truncate text if too long (to save tokens)
    max_text_length = 4000
    if len(text) > max_text_length:
        text = text[:max_text_length] + "..."

    prompt = f"""Analyze the following business website content and extract exactly {count} most relevant keywords that would help potential customers find this business.

The keywords should be:
- Relevant to the business and its services
- Searchable terms customers might use
- Between 2-40 characters each
- Specific and actionable

Website content:
{text}

Return only a comma-separated list of {count} keywords, nothing else."""

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a keyword extraction expert. Extract relevant keywords from business content.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=200,
        )

        content = response.choices[0].message.content or ""
        # Parse comma-separated keywords
        keywords = [kw.strip() for kw in content.split(",") if kw.strip()]

        # Validate and clean keywords
        validated_keywords = []
        for keyword in keywords:
            keyword = keyword.strip()
            # Remove quotes if present
            keyword = keyword.strip('"\'')
            if 2 <= len(keyword) <= 40:
                validated_keywords.append(keyword)
            if len(validated_keywords) >= count:
                break

        # Ensure we have exactly the requested number
        while len(validated_keywords) < count:
            validated_keywords.append(f"Keyword{len(validated_keywords) + 1}")

        logger.info(f"Generated {len(validated_keywords)} keywords using OpenAI")
        return validated_keywords[:count]

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise

