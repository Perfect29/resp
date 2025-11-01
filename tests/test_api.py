"""Tests for API endpoints."""

import pytest

from app.services.store import store


class TestInitTarget:
    """Tests for target initialization endpoint."""

    def test_init_target_success(self, client) -> None:  # type: ignore
        """Test successful target initialization."""
        # Clear store before test
        all_targets = store.list_all()
        for target in all_targets:
            store.delete(target.id)

        response = client.post(
            "/api/targets/init",
            json={
                "businessName": "Test Business",
                "websiteUrl": "https://example.com",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "target" in data
        assert data["target"]["businessName"] == "Test Business"
        assert data["target"]["websiteUrl"] == "https://example.com"
        assert len(data["target"]["keywords"]) == 5
        assert len(data["target"]["prompts"]) >= 2

    def test_init_target_invalid_url(self, client) -> None:  # type: ignore
        """Test initialization with invalid URL."""
        response = client.post(
            "/api/targets/init",
            json={
                "businessName": "Test Business",
                "websiteUrl": "not-a-url",
            },
        )
        assert response.status_code == 400

    def test_init_target_localhost_blocked(self, client) -> None:  # type: ignore
        """Test that localhost URLs are blocked."""
        response = client.post(
            "/api/targets/init",
            json={
                "businessName": "Test Business",
                "websiteUrl": "http://localhost:8000",
            },
        )
        assert response.status_code == 400


class TestGetTarget:
    """Tests for getting a target."""

    def test_get_target_success(self, client) -> None:  # type: ignore
        """Test successfully getting a target."""
        # First create a target
        init_response = client.post(
            "/api/targets/init",
            json={
                "businessName": "Test Business 2",
                "websiteUrl": "https://example.com",
            },
        )
        assert init_response.status_code == 201
        target_id = init_response.json()["target"]["id"]

        # Then get it
        response = client.get(f"/api/targets/{target_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == target_id
        assert data["businessName"] == "Test Business 2"

    def test_get_target_not_found(self, client) -> None:  # type: ignore
        """Test getting a non-existent target."""
        response = client.get("/api/targets/nonexistent-id")
        assert response.status_code == 404


class TestUpdateKeywords:
    """Tests for updating keywords."""

    def test_update_keywords_success(self, client) -> None:  # type: ignore
        """Test successfully updating keywords."""
        # First create a target
        init_response = client.post(
            "/api/targets/init",
            json={
                "businessName": "Test Business 3",
                "websiteUrl": "https://example.com",
            },
        )
        target_id = init_response.json()["target"]["id"]

        # Update keywords
        response = client.put(
            f"/api/targets/{target_id}/keywords",
            json={"keywords": ["new1", "new2", "new3", "new4", "new5"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["keywords"]) == 5
        assert data["keywords"][0]["value"] == "new1"

    def test_update_keywords_too_many(self, client) -> None:  # type: ignore
        """Test updating with too many keywords."""
        # First create a target
        init_response = client.post(
            "/api/targets/init",
            json={
                "businessName": "Test Business 4",
                "websiteUrl": "https://example.com",
            },
        )
        target_id = init_response.json()["target"]["id"]

        # Try to update with too many keywords
        response = client.put(
            f"/api/targets/{target_id}/keywords",
            json={"keywords": ["kw1", "kw2", "kw3", "kw4", "kw5", "kw6"]},
        )
        assert response.status_code == 400


class TestAnalyzeTarget:
    """Tests for analyzing a target."""

    def test_analyze_target_success(self, client) -> None:  # type: ignore
        """Test successfully analyzing a target."""
        # First create a target
        init_response = client.post(
            "/api/targets/init",
            json={
                "businessName": "Test Business 5",
                "websiteUrl": "https://example.com",
            },
        )
        target_id = init_response.json()["target"]["id"]

        # Analyze
        response = client.post(f"/api/targets/{target_id}/analyze")
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        assert "visibilityScore" in data["score"]
        assert 0 <= data["score"]["visibilityScore"] <= 100
        assert data["score"]["totalChecks"] > 0





