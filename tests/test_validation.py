"""Tests for validation utilities."""

import pytest

from app.utils.validation import (
    validate_business_name,
    validate_keywords,
    validate_prompts,
    validate_url,
)


class TestURLValidation:
    """Tests for URL validation."""

    def test_valid_http_url(self) -> None:
        """Test valid HTTP URL."""
        url = "http://example.com"
        result = validate_url(url)
        assert result == "http://example.com"

    def test_valid_https_url(self) -> None:
        """Test valid HTTPS URL."""
        url = "https://example.com/path?query=value"
        result = validate_url(url)
        assert "https://example.com" in result

    def test_invalid_scheme(self) -> None:
        """Test invalid URL scheme."""
        with pytest.raises(ValueError, match="http or https"):
            validate_url("ftp://example.com")

    def test_empty_url(self) -> None:
        """Test empty URL."""
        with pytest.raises(ValueError):
            validate_url("")

    def test_no_netloc(self) -> None:
        """Test URL without netloc."""
        with pytest.raises(ValueError):
            validate_url("http://")


class TestBusinessNameValidation:
    """Tests for business name validation."""

    def test_valid_name(self) -> None:
        """Test valid business name."""
        name = "Acme Corporation"
        result = validate_business_name(name)
        assert result == "Acme Corporation"

    def test_name_too_short(self) -> None:
        """Test name too short."""
        with pytest.raises(ValueError):
            validate_business_name("A")

    def test_name_too_long(self) -> None:
        """Test name too long."""
        with pytest.raises(ValueError):
            validate_business_name("A" * 81)

    def test_empty_name(self) -> None:
        """Test empty name."""
        with pytest.raises(ValueError):
            validate_business_name("")

    def test_whitespace_only(self) -> None:
        """Test whitespace-only name."""
        with pytest.raises(ValueError):
            validate_business_name("   ")


class TestKeywordsValidation:
    """Tests for keywords validation."""

    def test_valid_keywords(self) -> None:
        """Test valid keywords."""
        keywords = ["keyword1", "keyword2", "keyword3"]
        result = validate_keywords(keywords)
        assert len(result) == 3

    def test_too_many_keywords(self) -> None:
        """Test too many keywords."""
        with pytest.raises(ValueError, match="Maximum 5 keywords"):
            validate_keywords(["kw1", "kw2", "kw3", "kw4", "kw5", "kw6"])

    def test_keyword_too_short(self) -> None:
        """Test keyword too short."""
        with pytest.raises(ValueError):
            validate_keywords(["k"])

    def test_keyword_too_long(self) -> None:
        """Test keyword too long."""
        with pytest.raises(ValueError):
            validate_keywords(["k" * 41])

    def test_empty_list(self) -> None:
        """Test empty keywords list."""
        with pytest.raises(ValueError):
            validate_keywords([])


class TestPromptsValidation:
    """Tests for prompts validation."""

    def test_valid_prompts(self) -> None:
        """Test valid prompts."""
        prompts = ["prompt1", "prompt2"]
        result = validate_prompts(prompts)
        assert len(result) == 2

    def test_too_many_prompts(self) -> None:
        """Test too many prompts."""
        prompts = [f"prompt{i}" for i in range(11)]
        with pytest.raises(ValueError, match="Maximum 10 prompts"):
            validate_prompts(prompts)

    def test_prompt_too_long(self) -> None:
        """Test prompt too long."""
        with pytest.raises(ValueError):
            validate_prompts(["p" * 201])

    def test_prompt_with_localhost(self) -> None:
        """Test prompt with localhost URL."""
        with pytest.raises(ValueError, match="internal/localhost"):
            validate_prompts(["Check http://localhost:8000"])





