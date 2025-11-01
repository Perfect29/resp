"""Response models for API endpoints."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class KeywordResponse(BaseModel):
    """Keyword response model."""

    value: str = Field(..., description="Keyword value")
    generated: bool = Field(..., description="Whether keyword was auto-generated")


class PromptResponse(BaseModel):
    """Prompt response model."""

    value: str = Field(..., description="Prompt value")
    generated: bool = Field(..., description="Whether prompt was auto-generated")


class TargetResponse(BaseModel):
    """Target response model."""

    id: str = Field(..., description="Target ID")
    businessName: str = Field(..., description="Business name")
    websiteUrl: str = Field(..., description="Website URL")
    keywords: List[KeywordResponse] = Field(..., description="Keywords")
    prompts: List[PromptResponse] = Field(..., description="Prompts")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")


class InitTargetResponse(BaseModel):
    """Response model for initializing a target."""

    target: TargetResponse = Field(..., description="Created target")
    message: str = Field(default="Target initialized successfully")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error detail")





