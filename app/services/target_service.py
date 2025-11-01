"""Business logic for target management."""

import logging
from typing import List

from app.errors.http_errors import NotFoundError
from app.llm.keyword_gen import generate_keywords
from app.llm.prompts_builder import build_default_prompts
from app.models.response_models import TargetResponse
from app.services.store import store
from app.utils.extract_text import extract_text_from_html
from app.utils.fetch_page import fetch_page_content
from app.utils.sanitize_keywords import sanitize_keywords
from app.utils.validation import (
    validate_business_name,
    validate_keywords,
    validate_prompts,
    validate_url,
)

logger = logging.getLogger(__name__)


class TargetService:
    """Service for managing targets."""

    async def init_target(self, business_name: str, website_url: str) -> TargetResponse:
        """
        Initialize a new target by crawling website and generating keywords/prompts.

        Args:
            business_name: Business name
            website_url: Website URL

        Returns:
            Created TargetResponse

        Raises:
            ValueError: If validation fails
        """
        logger.info(f"Initializing target for {business_name} at {website_url}")

        # Validate inputs
        validated_name = validate_business_name(business_name)
        validated_url = validate_url(website_url)

        # Fetch and extract content
        logger.info(f"Fetching content from {validated_url}")
        text_content = None
        try:
            html_content = await fetch_page_content(validated_url)
            text_content = extract_text_from_html(html_content)
        except ValueError as e:
            # If website blocks access (403, etc.), use fallback content
            error_msg = str(e)
            if "403" in error_msg or "Forbidden" in error_msg:
                logger.warning(f"Website blocked access (403), using fallback content for {validated_name}")
                text_content = f"{validated_name} provides services and solutions. {validated_name} is a business offering various products and services to customers."
            else:
                # For other errors, also use fallback but log the issue
                logger.warning(f"Could not fetch content: {e}, using fallback content")
                text_content = f"{validated_name} provides services and solutions. {validated_name} is a business offering various products and services to customers."
        except Exception as e:
            logger.warning(f"Unexpected error fetching content: {e}, using fallback")
            text_content = f"{validated_name} provides services and solutions. {validated_name} is a business offering various products and services to customers."

        if not text_content or len(text_content) < 50:
            logger.warning("Extracted text content is too short, using fallback")
            text_content = f"{validated_name} provides services and solutions. {validated_name} is a business offering various products and services to customers."

        # Generate keywords
        logger.info("Generating keywords from content")
        try:
            raw_keywords = await generate_keywords(text_content, count=5)
        except Exception as e:
            logger.error(f"Error generating keywords: {e}", exc_info=True)
            # Use fallback keywords if generation fails
            raw_keywords = [
                validated_name,
                f"{validated_name} services",
                f"{validated_name} solutions",
                "business services",
                "professional services",
            ]
            logger.warning(f"Using fallback keywords: {raw_keywords}")
        
        sanitized_keywords = sanitize_keywords(raw_keywords)

        # Ensure we have exactly 5 keywords
        while len(sanitized_keywords) < 5:
            sanitized_keywords.append(f"{validated_name} {len(sanitized_keywords) + 1}")

        sanitized_keywords = sanitized_keywords[:5]

        # Build prompts
        logger.info("Building default prompts")
        try:
            prompts = await build_default_prompts(validated_name, sanitized_keywords)
        except Exception as e:
            logger.error(f"Error building prompts: {e}", exc_info=True)
            # Use fallback prompts if generation fails
            prompts = [
                f"What are the best {sanitized_keywords[0] if sanitized_keywords else 'services'}?",
                f"Top {sanitized_keywords[0] if sanitized_keywords else 'services'} recommendations",
                f"Compare {sanitized_keywords[0] if sanitized_keywords else 'services'} options",
                f"Which {sanitized_keywords[0] if sanitized_keywords else 'services'} should I choose?",
                f"Best {sanitized_keywords[0] if sanitized_keywords else 'services'} alternatives",
            ]
            logger.warning(f"Using fallback prompts: {prompts}")

        # Create target in store
        target = store.create(
            business_name=validated_name,
            website_url=validated_url,
            keywords=sanitized_keywords,
            prompts=prompts,
        )

        logger.info(f"Target initialized successfully: {target.id}")
        return target

    def get_target(self, target_id: str) -> TargetResponse:
        """
        Get a target by ID.

        Args:
            target_id: Target ID

        Returns:
            TargetResponse

        Raises:
            NotFoundError: If target not found
        """
        target = store.get(target_id)
        if not target:
            raise NotFoundError("target", target_id)
        return target

    async def update_keywords(self, target_id: str, keywords: List[str]) -> TargetResponse:
        """
        Update keywords for a target and regenerate prompts.

        Args:
            target_id: Target ID
            keywords: New keywords list

        Returns:
            Updated TargetResponse

        Raises:
            NotFoundError: If target not found
            ValueError: If validation fails
        """
        logger.info(f"Updating keywords for target {target_id}")

        # Check target exists
        target = self.get_target(target_id)

        # Validate keywords
        validated_keywords = validate_keywords(keywords)

        # Regenerate prompts based on new keywords
        logger.info("Regenerating prompts from new keywords")
        new_prompts = await build_default_prompts(target.businessName, validated_keywords)

        # Update keywords
        updated_target = store.update_keywords(
            target_id, validated_keywords, regenerate_prompts=True
        )

        if not updated_target:
            raise NotFoundError("target", target_id)

        # Update prompts separately
        updated_target = store.update_prompts(target_id, new_prompts)

        if not updated_target:
            raise NotFoundError("target", target_id)

        logger.info(f"Keywords updated successfully for target {target_id}")
        return updated_target

    def update_prompts(self, target_id: str, prompts: List[str]) -> TargetResponse:
        """
        Update prompts for a target.

        Args:
            target_id: Target ID
            prompts: New prompts list

        Returns:
            Updated TargetResponse

        Raises:
            NotFoundError: If target not found
            ValueError: If validation fails
        """
        logger.info(f"Updating prompts for target {target_id}")

        # Check target exists
        self.get_target(target_id)  # Will raise NotFoundError if not found

        # Validate prompts
        validated_prompts = validate_prompts(prompts)

        # Update prompts
        updated_target = store.update_prompts(target_id, validated_prompts)

        if not updated_target:
            raise NotFoundError("target", target_id)

        logger.info(f"Prompts updated successfully for target {target_id}")
        return updated_target


# Global service instance
target_service = TargetService()

