"""Visibility scoring calculations."""

import logging
from typing import List, Optional

from app.models.metrics_models import VisibilityCheck, VisibilityScore

logger = logging.getLogger(__name__)


def calculate_visibility_score(checks: List[VisibilityCheck]) -> VisibilityScore:
    """
    Calculate overall visibility score from check results.

    Uses sophisticated scoring algorithm that considers:
    - Occurrence rate (40% weight)
    - Position ranking (30% weight) 
    - Context relevance (30% weight)

    Args:
        checks: List of visibility check results

    Returns:
        VisibilityScore with calculated metrics
    """
    logger.info(f"📈 Calculating visibility score from {len(checks)} checks")

    total_checks = len(checks)
    if total_checks == 0:
        return VisibilityScore(
            totalChecks=0,
            occurrences=0,
            averagePosition=None,
            averageContextRelevance=0.0,
            visibilityScore=0.0,
            checks=[],
        )

    occurrences = sum(1 for check in checks if check.occurred)

    # Calculate average position (only for occurred checks)
    occurred_positions = [check.position for check in checks if check.position is not None]
    average_position: Optional[float] = None
    if occurred_positions:
        average_position = sum(occurred_positions) / len(occurred_positions)

    # Calculate average context relevance
    average_context_relevance = (
        sum(check.contextRelevance for check in checks) / total_checks
    )

    # Calculate visibility score (0-100) with improved algorithm
    # Formula: (occurrence_rate * 40) + (position_score * 30) + (relevance * 30)
    occurrence_rate = occurrences / total_checks  # 0.0-1.0

    # Enhanced position score based on BRAND RANK among competitors
    # Slightly tougher scoring for more realistic metrics
    position_score = 0.0
    if average_position is not None:
        # Position is now RANK among brands (1st brand = 1, 2nd brand = 2, etc.)
        if average_position <= 3:
            # Excellent: Top 3 brands (highest visibility) - slightly reduced from 1.0
            position_score = 0.92 - ((average_position - 1) / 2) * 0.05  # 0.92 to 0.87
        elif average_position <= 6:
            # Good: Positions 4-6 (visible but not top tier) - slightly reduced
            position_score = 0.70 - ((average_position - 3) / 3) * 0.18  # 0.70 to 0.52
        elif average_position <= 10:
            # Fair: Positions 7-10 (lower visibility, penalty starts) - slightly reduced
            position_score = 0.55 - ((average_position - 6) / 4) * 0.25  # 0.55 to 0.30
        elif average_position <= 15:
            # Poor: Positions 11-15 (low visibility, heavy penalty) - slightly reduced
            position_score = 0.30 - ((average_position - 10) / 5) * 0.18  # 0.30 to 0.12
        else:
            # Very poor: 16+ (almost invisible, minimal score)
            position_score = 0.05

    # Enhanced visibility score calculation - Slightly tougher for more realistic metrics
    # Optimal weights for user visibility (positions and mentions are critical):
    # - Occurrence rate (50%): Does brand appear? If not mentioned, score decreases significantly
    # - Position score (42%): Where does it appear? Early = excellent, late = heavy penalty
    # - Context relevance (8%): How well mentioned? Very low weight - positions/mentions matter more
    #
    # Key: Bad positioning (late appearance) AND not being mentioned significantly reduce score
    visibility_score = (
        (occurrence_rate * 50.0)
        + (position_score * 42.0)
        + (average_context_relevance * 8.0)
    )
    
    # Additional penalties for poor visibility (slightly increased)
    # 1. Late position penalty (if average position is bad - rank > 5, not 6)
    if average_position is not None and average_position > 5:
        # Position 6+ gets penalty (not in top tier) - starts earlier
        late_position_penalty = min(0.28, (average_position - 5) / 9.0)  # Slightly increased
        visibility_score = visibility_score * (1.0 - late_position_penalty)
    
    # 2. Not mentioned penalty (if occurrence rate is low) - slightly increased threshold
    if occurrence_rate < 0.55:  # Less than 55% (increased from 50%)
        missing_penalty = (0.55 - occurrence_rate) * 0.32  # Up to ~18% penalty (increased)
        visibility_score = visibility_score * (1.0 - missing_penalty)
    
    # 3. Small overall reduction for more conservative scoring (5% reduction)
    visibility_score = visibility_score * 0.95
    
    # Ensure score is within bounds (0-100)
    visibility_score = max(0.0, min(100.0, visibility_score))

    penalty_notes = []
    if average_position is not None and average_position > 5:
        late_penalty = min(0.28, (average_position - 5) / 9.0)
        penalty_notes.append(f"Rank >5: -{(late_penalty*100):.1f}%")
    
    if occurrence_rate < 0.55:
        missing_penalty = (0.55 - occurrence_rate) * 0.32
        penalty_notes.append(f"Low mentions: -{(missing_penalty*100):.1f}%")
    
    penalty_notes.append("Conservative: -5%")
    
    penalty_str = f" ({', '.join(penalty_notes)})" if penalty_notes else ""
    
    # Format position display
    position_display = f"Rank #{average_position}" if average_position else "N/A"
    
    logger.info(
        f"📊 Visibility score calculated: {visibility_score:.2f}/100{penalty_str}\n"
        f"   • Occurrence rate: {(occurrence_rate*100):.1f}% ({occurrences}/{total_checks}) [50% weight]\n"
        f"   • Position score: {position_score:.2f} "
        f"(avg rank: {position_display}) [42% weight]\n"
        f"   • Context relevance: {(average_context_relevance*100):.1f}% [8% weight]"
    )

    return VisibilityScore(
        totalChecks=total_checks,
        occurrences=occurrences,
        averagePosition=average_position,
        averageContextRelevance=average_context_relevance,
        visibilityScore=round(visibility_score, 2),
        checks=checks,
    )





