"""Prompt building utilities for visibility analysis with OpenAI integration."""

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


async def build_default_prompts(business_name: str, keywords: List[str]) -> List[str]:
    """
    Build default prompts for visibility analysis.

    Uses OpenAI API if API key is configured, otherwise falls back to
    simple prompt templates.

    Args:
        business_name: Business name
        keywords: List of keywords

    Returns:
        List of default prompts
    """
    logger.info(
        f"Building default prompts for '{business_name}' with {len(keywords)} keywords"
    )

    # Check OpenAI availability
    logger.info(f"OpenAI library available: {openai_available}")
    logger.info(f"API key configured: {bool(settings.openai_api_key and settings.openai_api_key.strip())}")

    # Use OpenAI if API key is available
    if (
        openai_available
        and settings.openai_api_key
        and settings.openai_api_key.strip()
    ):
        logger.info("🚀 Using OpenAI API to generate prompts")
        try:
            result = await _build_prompts_with_openai(business_name, keywords)
            logger.info(f"✅ Successfully generated {len(result)} prompts using OpenAI")
            return result
        except Exception as e:
            logger.error(f"❌ OpenAI prompt generation failed: {e}", exc_info=True)
            logger.warning("Falling back to stub implementation")
            # Fall through to stub implementation
    else:
        logger.warning("⚠️ OpenAI API key not configured, using stub implementation")

    # Fallback to simple templates

    prompts: List[str] = []

    # Generate user-focused prompts - what users actually search for
    # Focus on category/service type queries where business appears among competitors
    base_prompts = [
        f"Best {keywords[0] if keywords else 'services'}",
        f"Top {keywords[0] if keywords else 'services'} recommendations",
    ]

    # Add keyword-based prompts - user search patterns
    for keyword in keywords[:3]:  # Use first 3 keywords
        prompts.append(f"What are the best {keyword} services?")
        prompts.append(f"Compare top {keyword} platforms")
        if len(prompts) >= 4:
            break

    # Combine and deduplicate
    all_prompts = base_prompts + prompts
    unique_prompts = []
    seen = set()
    for prompt in all_prompts:
        if prompt not in seen and len(prompt) <= 200:
            unique_prompts.append(prompt)
            seen.add(prompt)
            if len(unique_prompts) >= 5:
                break

    # Ensure at least 2 prompts - use category queries, NOT brand-specific
    while len(unique_prompts) < 2:
        if keywords:
            unique_prompts.append(f"What are the best {keywords[0]} services?")
        else:
            unique_prompts.append("What are the best services in this category?")

    logger.info(f"Built {len(unique_prompts)} prompts")
    return unique_prompts[:5]  # Max 5 prompts for MVP


async def _build_prompts_with_openai(
    business_name: str, keywords: List[str]
) -> List[str]:
    """
    Build prompts using OpenAI API.

    Args:
        business_name: Business name
        keywords: List of keywords

    Returns:
        List of generated prompts
    """
    if not openai_available:
        raise ImportError("OpenAI library not available")

    client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=settings.openai_timeout)

    keywords_str = ", ".join(keywords[:5])  # Use up to 5 keywords

    prompt = f"""Generate exactly 5 search prompts that real users would type into AI assistants (ChatGPT, Claude, Perplexity) to find or compare services in the "{keywords_str}" category.

CRITICAL REQUIREMENTS:
1. Do NOT include "{business_name}" in the prompts - we want to see if it appears naturally in responses
2. Focus on CATEGORY/SERVICE TYPE queries (e.g., "best music streaming services", not "best Spotify")
3. Prompts should generate responses where MULTIPLE brands are mentioned
4. Under 200 characters each
5. Natural, real user language

GOOD examples (what users actually search):
- "What are the best {keywords_str}?"
- "Compare top {keywords_str} platforms"
- "Which {keywords_str} should I choose?"
- "Top {keywords_str} recommendations"
- "Alternatives to popular {keywords_str}"

BAD examples (DO NOT generate):
- "Tell me about {business_name}" ❌
- "{business_name} vs competitors" ❌
- "Is {business_name} good?" ❌

Return exactly 5 category-based prompts, one per line, nothing else. Each prompt should be a natural user query about the service category."""

    logger.info(f"📤 Sending prompt generation request to OpenAI (model: {settings.openai_model})")
    logger.info(f"Request prompt preview: {prompt[:200]}...")
    logger.info(f"API Key (first 10 chars): {settings.openai_api_key[:10]}..." if settings.openai_api_key else "No API key")
    
    # Log the full request for debugging
    request_data = {
        "model": settings.openai_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a search optimization expert. Generate natural search prompts for finding businesses.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.5,
        "max_tokens": 500,
    }
    logger.info(f"Full request to OpenAI: model={settings.openai_model}, message_length={len(prompt)}")

    try:
        response = await client.chat.completions.create(**request_data)
        
        # Log response details
        logger.info(f"✅ Received response from OpenAI API")
        logger.info(f"Response ID: {response.id}")
        logger.info(f"Response model: {response.model}")
        logger.info(f"Response usage: {response.usage.prompt_tokens} prompt tokens, {response.usage.completion_tokens} completion tokens")
        logger.info(f"Response content length: {len(response.choices[0].message.content or '')} chars")
        
        # This should appear in OpenAI dashboard
        logger.info(f"🔗 Check OpenAI dashboard for request ID: {response.id}")

        content = response.choices[0].message.content or ""
        logger.debug(f"Raw OpenAI response:\n{content}")
        
        # Parse prompts (one per line) - be more flexible with parsing
        raw_lines = content.split("\n")
        prompts = []
        
        for line in raw_lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove list markers (1., 2., -, *, •, etc.)
            # Handle numbered lists: "1. prompt", "2. prompt"
            if re.match(r'^\d+[.)]\s*', line):
                line = re.sub(r'^\d+[.)]\s*', '', line).strip()
            # Handle bullet points
            elif line.startswith("- ") or line.startswith("* "):
                line = line[2:].strip()
            elif line.startswith("• "):
                line = line[2:].strip()
            
            # Validate prompt
            if line and len(line) <= 200 and len(line) >= 10:
                # Remove quotes if wrapped
                line = line.strip('"\'')
                if line not in prompts:  # Avoid duplicates
                    prompts.append(line)
                    if len(prompts) >= 5:
                        break

        # Ensure we have exactly 5 prompts - fill with category queries if needed
        while len(prompts) < 5:
            if keywords:
                fallback = f"What are the best {keywords[len(prompts) % len(keywords)]} services?"
            else:
                fallback = "What are the best services in this category?"
            
            if fallback not in prompts:
                prompts.append(fallback)

        logger.info(f"Generated {len(prompts)} prompts using OpenAI")
        return prompts[:5]  # Return exactly 5 prompts

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise

