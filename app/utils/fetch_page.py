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
            # Use a more realistic browser User-Agent to avoid blocking
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            if status_code == 403:
                logger.error(f"Website blocked request (403 Forbidden) for {url}")
                raise ValueError(
                    f"Website {url} blocked the request (403 Forbidden). "
                    f"This website may restrict automated access. Please try a different website or contact support."
                ) from e
            elif status_code == 404:
                logger.error(f"Website not found (404) for {url}")
                raise ValueError(
                    f"Website not found (404) at {url}. Please check the URL is correct."
                ) from e
            else:
                logger.error(f"HTTP error fetching {url}: {e}")
                raise ValueError(
                    f"Cannot access website: HTTP {status_code}. Please check the URL is correct and accessible."
                ) from e
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching {url}")
            raise ValueError(
                f"Request to {url} timed out. The website may be slow or unreachable. Please try again."
            )
        except httpx.RequestError as e:
            logger.error(f"Request error fetching {url}: {e}")
            raise ValueError(
                f"Cannot reach website: {str(e)}. Please check the URL is correct and the website is online."
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            raise ValueError(f"Failed to fetch website: {str(e)}") from e





