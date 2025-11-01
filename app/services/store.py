"""In-memory storage for targets."""

import logging
from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from app.models.response_models import KeywordResponse, PromptResponse, TargetResponse

logger = logging.getLogger(__name__)


class TargetStore:
    """In-memory storage for targets."""

    def __init__(self) -> None:
        """Initialize the store."""
        self._targets: Dict[str, TargetResponse] = {}
        logger.info("TargetStore initialized")

    def create(
        self,
        business_name: str,
        website_url: str,
        keywords: list[str],
        prompts: list[str],
    ) -> TargetResponse:
        """
        Create a new target.

        Args:
            business_name: Business name
            website_url: Website URL
            keywords: List of keyword strings
            prompts: List of prompt strings

        Returns:
            Created TargetResponse
        """
        target_id = str(uuid4())
        now = datetime.utcnow()

        keyword_responses = [
            KeywordResponse(value=k, generated=True) for k in keywords
        ]
        prompt_responses = [
            PromptResponse(value=p, generated=True) for p in prompts
        ]

        target = TargetResponse(
            id=target_id,
            businessName=business_name,
            websiteUrl=website_url,
            keywords=keyword_responses,
            prompts=prompt_responses,
            createdAt=now,
            updatedAt=now,
        )

        self._targets[target_id] = target
        logger.info(f"Created target: {target_id} for {business_name}")

        return target

    def get(self, target_id: str) -> Optional[TargetResponse]:
        """
        Get a target by ID.

        Args:
            target_id: Target ID

        Returns:
            TargetResponse if found, None otherwise
        """
        return self._targets.get(target_id)

    def update_keywords(
        self, target_id: str, keywords: list[str], regenerate_prompts: bool = True
    ) -> Optional[TargetResponse]:
        """
        Update keywords for a target.

        Args:
            target_id: Target ID
            keywords: New keywords list
            regenerate_prompts: Whether to regenerate prompts

        Returns:
            Updated TargetResponse if found, None otherwise
        """
        target = self._targets.get(target_id)
        if not target:
            return None

        keyword_responses = [
            KeywordResponse(value=k, generated=False) for k in keywords
        ]

        # If regenerating prompts, we'll need to rebuild them
        # For now, just update keywords
        prompt_responses = target.prompts.copy()

        updated_target = TargetResponse(
            id=target.id,
            businessName=target.businessName,
            websiteUrl=target.websiteUrl,
            keywords=keyword_responses,
            prompts=prompt_responses,
            createdAt=target.createdAt,
            updatedAt=datetime.utcnow(),
        )

        self._targets[target_id] = updated_target
        logger.info(f"Updated keywords for target: {target_id}")

        return updated_target

    def update_prompts(
        self, target_id: str, prompts: list[str]
    ) -> Optional[TargetResponse]:
        """
        Update prompts for a target.

        Args:
            target_id: Target ID
            prompts: New prompts list

        Returns:
            Updated TargetResponse if found, None otherwise
        """
        target = self._targets.get(target_id)
        if not target:
            return None

        prompt_responses = [
            PromptResponse(value=p, generated=False) for p in prompts
        ]

        updated_target = TargetResponse(
            id=target.id,
            businessName=target.businessName,
            websiteUrl=target.websiteUrl,
            keywords=target.keywords.copy(),
            prompts=prompt_responses,
            createdAt=target.createdAt,
            updatedAt=datetime.utcnow(),
        )

        self._targets[target_id] = updated_target
        logger.info(f"Updated prompts for target: {target_id}")

        return updated_target

    def list_all(self) -> list[TargetResponse]:
        """
        List all targets.

        Returns:
            List of all TargetResponse objects
        """
        return list(self._targets.values())

    def delete(self, target_id: str) -> bool:
        """
        Delete a target.

        Args:
            target_id: Target ID

        Returns:
            True if deleted, False if not found
        """
        if target_id in self._targets:
            del self._targets[target_id]
            logger.info(f"Deleted target: {target_id}")
            return True
        return False


# Global store instance
store = TargetStore()





