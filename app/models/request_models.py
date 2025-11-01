"""Request models for API endpoints."""

from typing import List

from pydantic import BaseModel, Field, field_validator


class InitTargetRequest(BaseModel):
    """Request model for initializing a new target."""

    businessName: str = Field(
        ..., description="Business name", min_length=2, max_length=80
    )
    websiteUrl: str = Field(..., description="Website URL")

    @field_validator("businessName")
    @classmethod
    def validate_business_name(cls, v: str) -> str:
        """Validate business name."""
        if not v.strip():
            raise ValueError("Business name cannot be empty or whitespace only")
        return v.strip()


class UpdateKeywordsRequest(BaseModel):
    """Request model for updating keywords."""

    keywords: List[str] = Field(
        ..., description="List of keywords", min_length=1, max_length=5
    )

    @field_validator("keywords", mode="before")
    @classmethod
    def validate_keywords(cls, v: List[str]) -> List[str]:
        """Validate keywords list."""
        if not isinstance(v, list):
            raise ValueError("Keywords must be a list")
        if len(v) > 5:
            raise ValueError("Maximum 5 keywords allowed")
        if len(v) < 1:
            raise ValueError("At least 1 keyword required")
        return v

    @field_validator("keywords")
    @classmethod
    def validate_keyword_items(cls, v: List[str]) -> List[str]:
        """Validate individual keyword items."""
        validated = []
        for keyword in v:
            if not isinstance(keyword, str):
                raise ValueError("All keywords must be strings")
            keyword = keyword.strip()
            if len(keyword) < 2 or len(keyword) > 40:
                raise ValueError(
                    "Each keyword must be between 2 and 40 characters"
                )
            if not keyword:
                raise ValueError("Keywords cannot be empty")
            validated.append(keyword)
        return validated


class UpdatePromptsRequest(BaseModel):
    """Request model for updating prompts."""

    prompts: List[str] = Field(
        ..., description="List of prompts", min_length=1, max_length=5
    )

    @field_validator("prompts", mode="before")
    @classmethod
    def validate_prompts(cls, v: List[str]) -> List[str]:
        """Validate prompts list."""
        if not isinstance(v, list):
            raise ValueError("Prompts must be a list")
        if len(v) > 10:
            raise ValueError("Maximum 10 prompts allowed")
        if len(v) < 1:
            raise ValueError("At least 1 prompt required")
        return v

    @field_validator("prompts")
    @classmethod
    def validate_prompt_items(cls, v: List[str]) -> List[str]:
        """Validate individual prompt items."""
        validated = []
        for prompt in v:
            if not isinstance(prompt, str):
                raise ValueError("All prompts must be strings")
            prompt = prompt.strip()
            if len(prompt) > 200:
                raise ValueError("Each prompt must be 200 characters or less")
            if not prompt:
                raise ValueError("Prompts cannot be empty")
            validated.append(prompt)
        return validated





