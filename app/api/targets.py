"""Target management API endpoints."""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.errors.http_errors import NotFoundError
from app.metrics.sampler import check_visibility_with_openai
from app.metrics.scorer import calculate_visibility_score
from app.models.metrics_models import AnalyzeResponse, VisibilityCheck
from app.models.request_models import (
    InitTargetRequest,
    UpdateKeywordsRequest,
    UpdatePromptsRequest,
)
from app.models.response_models import InitTargetResponse, TargetResponse
from app.services.target_service import target_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/targets", tags=["targets"])


@router.post("/init", response_model=InitTargetResponse, status_code=201)
async def init_target(request: InitTargetRequest) -> InitTargetResponse:
    """
    Initialize a new target by crawling website and generating keywords/prompts.

    Args:
        request: InitTargetRequest with businessName and websiteUrl

    Returns:
        InitTargetResponse with created target

    Raises:
        HTTPException: If initialization fails
    """
    try:
        target = await target_service.init_target(
            business_name=request.businessName, website_url=request.websiteUrl
        )

        return InitTargetResponse(target=target)

    except ValueError as e:
        logger.error(f"Validation error initializing target: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        logger.error(f"Not found error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error initializing target: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to initialize target")


@router.get("/{target_id}", response_model=TargetResponse)
async def get_target(target_id: str) -> TargetResponse:
    """
    Get a target by ID.

    Args:
        target_id: Target ID

    Returns:
        TargetResponse

    Raises:
        HTTPException: If target not found
    """
    try:
        return target_service.get_target(target_id)
    except NotFoundError as e:
        logger.warning(f"Target not found: {target_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error getting target: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get target")


@router.put("/{target_id}/keywords", response_model=TargetResponse)
async def update_keywords(
    target_id: str, request: UpdateKeywordsRequest
) -> TargetResponse:
    """
    Update keywords for a target and regenerate prompts.

    Args:
        target_id: Target ID
        request: UpdateKeywordsRequest with keywords list

    Returns:
        Updated TargetResponse

    Raises:
        HTTPException: If update fails
    """
    try:
        return await target_service.update_keywords(target_id, request.keywords)
    except NotFoundError as e:
        logger.warning(f"Target not found: {target_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"Validation error updating keywords: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating keywords: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update keywords")


@router.put("/{target_id}/prompts", response_model=TargetResponse)
async def update_prompts(
    target_id: str, request: UpdatePromptsRequest
) -> TargetResponse:
    """
    Update prompts for a target.

    Args:
        target_id: Target ID
        request: UpdatePromptsRequest with prompts list

    Returns:
        Updated TargetResponse

    Raises:
        HTTPException: If update fails
    """
    try:
        return target_service.update_prompts(target_id, request.prompts)
    except NotFoundError as e:
        logger.warning(f"Target not found: {target_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"Validation error updating prompts: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating prompts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update prompts")


@router.post("/{target_id}/analyze", response_model=AnalyzeResponse)
async def analyze_target(target_id: str) -> AnalyzeResponse:
    """
    Analyze visibility for a target.

    Sends 6 real OpenAI API calls per prompt (max 5 prompts).
    Total: 30 API calls (5 prompts × 6 calls).
    
    Each call sends the prompt to OpenAI (max 200 chars) and checks if the keyword
    appears in the response. Response length is restricted to 300 tokens to manage costs.

    Args:
        target_id: Target ID

    Returns:
        AnalyzeResponse with visibility score

    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Get target
        target = target_service.get_target(target_id)

        # Limit to max 5 prompts for MVP
        prompts_to_analyze = target.prompts[:5]
        
        logger.info(
            f"🔍 Starting analysis for target {target_id} "
            f"(analyzing {len(prompts_to_analyze)} prompts with 6 checks each = {len(prompts_to_analyze) * 6} total checks)"
        )

        # Perform 6 checks per prompt (30 checks total: 5 prompts × 6 checks)
        checks: list[VisibilityCheck] = []
        total_checks = len(prompts_to_analyze) * 6

        for prompt_idx, prompt_resp in enumerate(prompts_to_analyze, 1):
            prompt = prompt_resp.value
            logger.info(f"  📝 Prompt {prompt_idx}/{len(prompts_to_analyze)}: '{prompt[:60]}...'")

            # Use BUSINESS NAME (brand) for analysis, not keywords
            # We want to see if the BRAND appears when users search for the category
            brand_name = target.businessName
            
            # Perform 6 checks for this prompt (each sends to OpenAI API)
            for check_index in range(6):
                occurred, position, context_relevance = await check_visibility_with_openai(
                    prompt=prompt,
                    keyword=brand_name,  # Check for BRAND name, not keyword
                    target_id=target_id,
                    check_index=check_index,
                )
                
                logger.debug(
                    f"    Check {check_index + 1}/6 for prompt '{prompt[:40]}...': "
                    f"occurred={occurred}, position={position}, relevance={context_relevance:.2f}"
                )

                checks.append(
                    VisibilityCheck(
                        prompt=prompt,
                        keyword=brand_name,  # Store brand name for tracking
                        occurred=occurred,
                        position=position,
                        contextRelevance=context_relevance,
                    )
                )
                
                current_check = (prompt_idx - 1) * 6 + check_index + 1
                logger.info(
                    f"    ✓ Check {current_check}/{total_checks}: "
                    f"prompt='{prompt[:40]}...' → "
                    f"{'✅ FOUND' if occurred else '❌ NOT FOUND'} "
                    f"(pos: {position or 'N/A'}, relevance: {context_relevance:.2f})"
                )

        # Calculate visibility score
        score = calculate_visibility_score(checks)

        # Log detailed results
        logger.info(
            f"✅ Analysis complete for target {target_id}:\n"
            f"   📊 Total checks: {score.totalChecks} (5 prompts × 6 checks = 30)\n"
            f"   ✅ Occurrences: {score.occurrences} "
            f"({(score.occurrences/score.totalChecks*100):.1f}%)\n"
            f"   📍 Avg position: {score.averagePosition or 'N/A'}\n"
            f"   🎯 Visibility score: {score.visibilityScore:.2f}/100"
        )

        return AnalyzeResponse(
            targetId=target_id,
            score=score,
            analyzedAt=datetime.utcnow().isoformat(),
        )

    except NotFoundError as e:
        logger.warning(f"Target not found for analysis: {target_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error analyzing target: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to analyze target")

