"""SSRF protection utilities to block localhost and private IPs."""

import ipaddress
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def is_private_ip(ip: str) -> bool:
    """
    Check if IP address is private or reserved.

    Args:
        ip: IP address string

    Returns:
        True if IP is private/reserved, False otherwise
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved
    except ValueError:
        return True  # Treat invalid IPs as private for safety


def is_localhost_hostname(hostname: str) -> bool:
    """
    Check if hostname is localhost or local.

    Args:
        hostname: Hostname string

    Returns:
        True if hostname is localhost/local, False otherwise
    """
    hostname_lower = hostname.lower()
    localhost_names = {
        "localhost",
        "127.0.0.1",
        "::1",
        "0.0.0.0",
        "local",
        ".local",
        ".localhost",
    }
    return (
        hostname_lower in localhost_names
        or hostname_lower.endswith(".local")
        or hostname_lower.endswith(".localhost")
    )


def check_ssrf_protection(url: str) -> None:
    """
    Check URL for SSRF vulnerabilities and block if unsafe.

    Args:
        url: URL string to check

    Raises:
        ValueError: If URL is blocked (localhost, private IP, etc.)
    """
    try:
        parsed = urlparse(url)

        if not parsed.netloc:
            raise ValueError("Invalid URL: missing hostname")

        hostname = parsed.hostname
        if not hostname:
            raise ValueError("Invalid URL: missing hostname")

        # Check localhost hostnames
        if is_localhost_hostname(hostname):
            logger.warning(f"SSRF protection: blocked localhost hostname: {hostname}")
            raise ValueError("Access to localhost is not allowed")

        # Try to resolve IP if hostname looks like IP
        try:
            # Check if hostname is an IP address
            ip_obj = ipaddress.ip_address(hostname)
            if is_private_ip(hostname):
                logger.warning(f"SSRF protection: blocked private IP: {hostname}")
                raise ValueError("Access to private IP addresses is not allowed")
        except ValueError:
            # Hostname is not an IP, which is generally safer
            # We'll validate DNS resolution is not done here for performance
            # In production, you might want to do DNS resolution check
            pass

        # Block common internal network patterns
        if hostname.startswith(("10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.", "192.168.")):
            logger.warning(f"SSRF protection: blocked suspicious hostname: {hostname}")
            raise ValueError("Access to private network addresses is not allowed")

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"SSRF protection check failed: {e}")
        raise ValueError("URL validation failed") from e





