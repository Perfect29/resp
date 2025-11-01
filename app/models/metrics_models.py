"""Models for visibility metrics and analysis."""

from typing import List, Optional

from pydantic import BaseModel, Field


class VisibilityCheck(BaseModel):
    """Single visibility check result."""

    prompt: str = Field(..., description="Prompt used")
    keyword: str = Field(..., description="Keyword checked")
    occurred: bool = Field(..., description="Whether keyword occurred in result")
    position: Optional[int] = Field(
        None, description="Position of keyword if occurred"
    )
    contextRelevance: float = Field(
        ..., description="Context relevance score (0.0-1.0)", ge=0.0, le=1.0
    )


class VisibilityScore(BaseModel):
    """Overall visibility score calculation."""

    totalChecks: int = Field(..., description="Total number of checks performed")
    occurrences: int = Field(..., description="Total occurrences found")
    averagePosition: Optional[float] = Field(
        None, description="Average position of occurrences"
    )
    averageContextRelevance: float = Field(
        ...,
        description="Average context relevance score",
        ge=0.0,
        le=1.0,
    )
    visibilityScore: float = Field(
        ...,
        description="Final visibility score (0.0-100.0)",
        ge=0.0,
        le=100.0,
    )
    checks: List[VisibilityCheck] = Field(..., description="Individual check results")


class AnalyzeResponse(BaseModel):
    """Response model for analysis endpoint."""

    targetId: str = Field(..., description="Target ID")
    score: VisibilityScore = Field(..., description="Visibility score")
    analyzedAt: str = Field(..., description="Analysis timestamp (ISO format)")





