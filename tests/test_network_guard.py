"""Tests for SSRF protection."""

import pytest

from app.utils.network_guard import check_ssrf_protection


class TestSSRFProtection:
    """Tests for SSRF protection."""

    def test_allows_public_url(self) -> None:
        """Test that public URLs are allowed."""
        check_ssrf_protection("https://example.com")  # Should not raise

    def test_blocks_localhost(self) -> None:
        """Test that localhost is blocked."""
        with pytest.raises(ValueError, match="localhost"):
            check_ssrf_protection("http://localhost:8000")

    def test_blocks_127_0_0_1(self) -> None:
        """Test that 127.0.0.1 is blocked."""
        with pytest.raises(ValueError, match="private"):
            check_ssrf_protection("http://127.0.0.1:8000")

    def test_blocks_private_ip_range_10(self) -> None:
        """Test that 10.x.x.x is blocked."""
        with pytest.raises(ValueError, match="private"):
            check_ssrf_protection("http://10.0.0.1")

    def test_blocks_private_ip_range_192_168(self) -> None:
        """Test that 192.168.x.x is blocked."""
        with pytest.raises(ValueError, match="private"):
            check_ssrf_protection("http://192.168.1.1")

    def test_blocks_private_ip_range_172_16(self) -> None:
        """Test that 172.16-31.x.x is blocked."""
        with pytest.raises(ValueError, match="private"):
            check_ssrf_protection("http://172.16.0.1")





