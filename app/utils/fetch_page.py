"""Web page fetching utilities."""

import logging
from typing import Optional

import httpx

from app.utils.network_guard import check_ssrf_protection

logger = logging.getLogger(__name__)


async def fetch_page_content(url: str, timeout: float = 10.0) -> str:
    """
    Fetch HTML content from a URL with SSRF protection.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        HTML content as string

    Raises:
        ValueError: If URL is blocked by SSRF protection or invalid
        httpx.HTTPError: If HTTP request fails
    """
    # Apply SSRF protection
    check_ssrf_protection(url)

    logger.info(f"Fetching page: {url}")

    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        try:
            response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching {url}: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error fetching {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            raise





