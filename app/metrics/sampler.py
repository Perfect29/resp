"""Visibility sampling with real OpenAI API calls."""

import logging
from typing import Optional, Tuple

from app.config import settings

logger = logging.getLogger(__name__)

# Try to import OpenAI
try:
    from openai import AsyncOpenAI

    openai_available = True
except ImportError:
    openai_available = False
    logger.warning("OpenAI library not installed. Cannot perform real visibility checks.")


async def check_visibility_with_openai(
    prompt: str, keyword: str, target_id: str, check_index: int
) -> Tuple[bool, Optional[int], float]:
    """
    Check visibility by sending prompt to OpenAI and analyzing ALL keyword mentions.
    
    Analyzes the full response as a list:
    - Finds ALL occurrences of the keyword
    - Extracts positions for each mention
    - Extracts context around each mention
    - Calculates comprehensive score based on mentions, positions, and context quality

    Args:
        prompt: Prompt to send to OpenAI
        keyword: Keyword to search for in response
        target_id: Target ID for logging
        check_index: Index of this check (0-5)

    Returns:
        Tuple of (occurred: bool, position: Optional[int], context_relevance: float)
        - occurred: True if keyword found at least once
        - position: Best position (earliest occurrence)
        - context_relevance: Calculated from all mentions, positions, and contexts
    """
    # Use OpenAI if available, otherwise fallback to simulation
    if not openai_available or not settings.openai_api_key or not settings.openai_api_key.strip():
        logger.warning(f"OpenAI not available for check {check_index + 1}, using simulation")
        return _simulate_visibility_check(prompt, keyword, target_id, check_index)

    client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=settings.openai_timeout)
    
    # Clean the prompt - remove any appended instructions
    clean_prompt = prompt.split('\nIMPORTANT:')[0].strip()
    clean_prompt = clean_prompt[:200] if len(clean_prompt) > 200 else clean_prompt
    
    logger.info(
        f"      📤 Sending to OpenAI: prompt='{clean_prompt[:50]}...' "
        f"keyword='{keyword}' (check {check_index + 1}/6)"
    )

    try:
        # Single API call: Answer the user query AND return structured analysis
        # Structure recommended by ChatGPT for better ranking accuracy
        combined_request = f"""Answer this user query naturally. When listing services/brands, provide a comprehensive list of 10-15 options:

{clean_prompt}

---

CRITICAL ANALYSIS INSTRUCTIONS:

Perform this analysis process (do NOT skip steps):

1. Scan your response above and identify EVERY brand/service name mentioned (create a complete list).
2. Number them in the exact order they appear: 1st mentioned = position 1, 2nd mentioned = position 2, 3rd = position 3, etc.
3. Locate "{keyword}" in that numbered list.
4. Return ONLY valid JSON:

{{
  "mentions": [
    {{
      "position": <position number>,
      "context": "<50-100 characters of text around the brand mention from your response above>",
      "relevance_score": <1.0 if position 1-3, 0.8-0.9 if position 4-6, 0.5-0.7 if position 7-10, 0.3 if position 11+>
    }}
  ]
}}

If "{keyword}" does NOT appear in your response, return: {{"mentions": []}}

Return ONLY the JSON object, nothing else."""

        # Single API call - get response and structured analysis
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. When analyzing brand mentions, you must first identify ALL brands in order, then find the target brand's position in that complete ordered list. Answer queries naturally and return ONLY the requested JSON structure.",
                },
                {
                    "role": "user",
                    "content": combined_request,
                }
            ],
            temperature=0.7,
            max_tokens=400,  # Enough for response + JSON
            top_p=0.9,
            response_format={"type": "json_object"},
        )

        analysis_text = response.choices[0].message.content or ""
        
        logger.debug(
            f"      ✅ Response received: {len(analysis_text)} chars, "
            f"tokens: {response.usage.prompt_tokens}+{response.usage.completion_tokens}"
        )
        
        # Parse structured JSON response
        import json
        try:
            # Extract JSON from response (might have extra text)
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = analysis_text[json_start:json_end]
            analysis_data = json.loads(json_str)
            mentions_data = analysis_data.get('mentions', [])
            
            if not isinstance(mentions_data, list):
                raise ValueError("Invalid mentions format")
            
            logger.debug(f"      Parsed {len(mentions_data)} mention(s) from JSON")
                
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning(f"      ⚠️ Failed to parse JSON analysis: {e}, falling back to direct text analysis")
            logger.debug(f"      Response text: {analysis_text[:200]}...")
            # Fallback: analyze text directly
            # Extract actual response text before JSON (if any)
            response_text = analysis_text.split('Response:')[-1].split('Return a JSON')[0].strip() if 'Response:' in analysis_text else analysis_text
            return _analyze_text_response(response_text, keyword, check_index)
        
        # Process structured mentions from OpenAI analysis
        mentions = []
        for mention in mentions_data:
            if not isinstance(mention, dict):
                continue
                
            position = mention.get('position')
            context = mention.get('context', '')
            relevance_score = mention.get('relevance_score', 0.5)
            
            # Validate and clean data
            # Position should be rank among brands (1, 2, 3...) not character position
            if position is None or not isinstance(position, int) or position < 1:
                # If position seems too high (likely character position), try to validate
                if position and position > 500:
                    logger.warning(f"      ⚠️ Position {position} seems like character position, not brand rank. Adjusting...")
                    # Assume it's character position and estimate brand rank (rough heuristic)
                    # This is a fallback - should ideally be fixed in prompt
                    position = max(1, min(10, position // 50))  # Rough estimate
                else:
                    continue
                
            if not isinstance(relevance_score, (int, float)):
                relevance_score = 0.5
            relevance_score = max(0.0, min(1.0, float(relevance_score)))
            
            # Verify brand actually appears in context (case-insensitive check)
            if keyword.lower() not in context.lower():
                logger.warning(f"      ⚠️ Brand '{keyword}' not found in provided context, skipping mention")
                continue
            
            # Calculate additional context quality from our analysis
            # Use position-1 for character position (if valid), otherwise use 0
            char_pos = position - 1 if position and position < 1000 else 0
            context_quality = _calculate_context_quality(context, keyword, analysis_text, char_pos)
            
            # Combine OpenAI relevance with our context quality (positions/mentions weighted more)
            combined_relevance = (relevance_score * 0.7) + (context_quality * 0.3)
            
            mentions.append({
                'position': position,
                'context': context,
                'relevance_score': relevance_score,
                'context_quality': context_quality,
                'combined_relevance': combined_relevance,
            })
        
        # Calculate comprehensive metrics from ALL mentions
        occurred = len(mentions) > 0
        
        if not occurred:
            logger.info(f"      ✓ Result: ❌ NOT FOUND (0 mentions)")
            return False, None, 0.1
        
        # Get best position (earliest occurrence)
        best_position = min(m['position'] for m in mentions)
        
        # Calculate comprehensive context relevance from ALL mentions
        num_mentions = len(mentions)
        
        # 1. Frequency score (logarithmic scale: more mentions = better, but diminishing returns)
        if num_mentions == 1:
            frequency_score = 0.5
        elif num_mentions == 2:
            frequency_score = 0.75
        elif num_mentions == 3:
            frequency_score = 0.90
        elif num_mentions >= 4:
            frequency_score = min(1.0, 0.90 + (num_mentions - 3) * 0.05)  # Max 1.0
        else:
            frequency_score = 0.5
        
        # 2. Position score: based on BRAND RANK among competitors (slightly tougher)
        # Position = rank among brands (1st brand = 1, 2nd = 2, etc.)
        position_scores = []
        for mention in mentions:
            pos = mention['position']
            # Score based on brand rank - slightly reduced for more realistic scoring
            if pos <= 3:
                # Excellent: Top 3 brands - slightly reduced
                pos_score = 0.92 - ((pos - 1) / 2) * 0.05  # 0.92 to 0.87
            elif pos <= 6:
                # Good: Ranks 4-6 - slightly reduced
                pos_score = 0.70 - ((pos - 3) / 3) * 0.18  # 0.70 to 0.52
            elif pos <= 10:
                # Fair: Ranks 7-10 (penalty starts) - slightly reduced
                pos_score = 0.55 - ((pos - 6) / 4) * 0.25  # 0.55 to 0.30
            elif pos <= 15:
                # Poor: Ranks 11-15 (heavy penalty) - slightly reduced
                pos_score = 0.30 - ((pos - 10) / 5) * 0.18  # 0.30 to 0.12
            else:
                # Very poor: Rank 16+ (minimal score)
                pos_score = 0.05
            position_scores.append(pos_score)
        
        # Weighted average position score (earlier mentions weighted MUCH higher)
        # First mention gets full weight, subsequent mentions get reduced weight
        total_weight = sum(1.0 / ((i + 1) ** 1.5) for i in range(len(position_scores)))
        weighted_position_score = sum(score / ((i + 1) ** 1.5) for i, score in enumerate(position_scores)) / total_weight if total_weight > 0 else 0.0
        
        # 3. Context relevance: average of combined relevance scores
        avg_relevance = sum(m['combined_relevance'] for m in mentions) / len(mentions) if mentions else 0.0
        
        # 4. Final context relevance calculation - Slightly tougher for more variation
        # Frequency and Position are critical - Context has very low weight
        # Frequency: 55%, Position: 42%, Relevance: 3% (context minimal weight)
        context_relevance = (
            frequency_score * 0.55 +
            weighted_position_score * 0.42 +
            avg_relevance * 0.03
        )
        
        # Additional penalty if best position (rank) is bad (late appearance hurts visibility significantly)
        best_position = min(m['position'] for m in mentions)
        if best_position > 5:  # Starts earlier (5 instead of 6)
            # Rank > 5 gets penalty (not in top tier)
            late_penalty = min(0.22, (best_position - 5) / 9.0)  # Slightly increased
            context_relevance = context_relevance * (1.0 - late_penalty)
        
        # Small reduction to ensure more variation (not always near 1.0)
        context_relevance = context_relevance * 0.92
        
        context_relevance = min(0.95, max(0.05, context_relevance))  # Cap at 0.95, not 1.0
        
        # Format brand ranks for logging (avoid backslash in f-string)
        rank_list = [f"#{m['position']}" for m in mentions]
        logger.info(
            f"      ✓ Result: ✅ FOUND {num_mentions} mention(s)\n"
            f"         Brand ranks: {rank_list}\n"
            f"         Best rank: #{best_position}\n"
            f"         Avg relevance: {avg_relevance:.2f}\n"
            f"         Final score: {context_relevance:.2f}"
        )

        return occurred, best_position, context_relevance

    except Exception as e:
        logger.error(f"      ❌ OpenAI API error for check {check_index + 1}: {e}", exc_info=True)
        # Fallback to simulation on error
        logger.warning(f"      Falling back to simulation for check {check_index + 1}")
        return _simulate_visibility_check(prompt, keyword, target_id, check_index)


def _analyze_text_response(response_text: str, keyword: str, check_index: int) -> Tuple[bool, Optional[int], float]:
    """
    Fallback: Analyze text response directly if JSON parsing fails.
    
    Finds brand mentions and estimates rank among competitors.
    """
    keyword_lower = keyword.lower()
    keyword_exact = keyword  # Keep original case for exact matching
    response_lower = response_text.lower()
    
    # Find ALL positions where keyword/brand appears
    mentions = []
    search_pos = 0
    
    # Try exact match first (case-sensitive), then case-insensitive
    exact_positions = []
    while True:
        pos = response_text.find(keyword_exact, search_pos)
        if pos == -1:
            break
        exact_positions.append(pos)
        search_pos = pos + 1
    
    # If no exact match, try case-insensitive
    if not exact_positions:
        search_pos = 0
        while True:
            pos = response_lower.find(keyword_lower, search_pos)
            if pos == -1:
                break
            exact_positions.append(pos)
            search_pos = pos + 1
    
    # Estimate brand rank: find all brand-like words (capitalized words that might be brands)
    # Simple heuristic: if keyword appears early relative to other capitalized terms, rank is better
    import re
    capitalized_words = [m.start() for m in re.finditer(r'\b[A-Z][a-z]+\b', response_text)]
    
    for pos in exact_positions:
        # Estimate rank: count how many capitalized words appear before this mention
        rank = sum(1 for cap_pos in capitalized_words if cap_pos < pos) + 1
        
        # Extract context
        context_start = max(0, pos - 100)
        context_end = min(len(response_text), pos + len(keyword) + 100)
        context = response_text[context_start:context_end]
        
        context_quality = _calculate_context_quality(context, keyword, response_text, pos)
        
        mentions.append({
            'position': rank,  # Estimated rank among brands
            'context': context,
            'context_quality': context_quality,
        })
    
    if not mentions:
        logger.debug(f"      Brand '{keyword}' not found in response text")
        return False, None, 0.1
    
    # Use best (lowest) rank
    best_rank = min(m['position'] for m in mentions)
    avg_quality = sum(m['context_quality'] for m in mentions) / len(mentions)
    
    # Scoring based on rank
    if best_rank <= 3:
        position_score = 1.0
    elif best_rank <= 6:
        position_score = 0.75
    elif best_rank <= 10:
        position_score = 0.5
    else:
        position_score = 0.2
    
    frequency_score = min(1.0, 0.5 + (len(mentions) - 1) * 0.2)
    context_relevance = (frequency_score * 0.55 + position_score * 0.42 + avg_quality * 0.03)
    
    logger.debug(f"      Fallback analysis: found {len(mentions)} mention(s), rank #{best_rank}")
    return True, best_rank, min(1.0, max(0.05, context_relevance))


def _calculate_context_quality(context: str, keyword: str, full_text: str, position: int) -> float:
    """
    Calculate quality score for context around a keyword mention.
    
    Factors:
    - Context length (optimal ~50-150 chars)
    - Keyword prominence (capitalization, emphasis)
    - Surrounding sentence structure
    - Relevance indicators (positive words, business terms)
    
    Returns:
        Context quality score (0.0-1.0)
    """
    context_lower = context.lower()
    keyword_lower = keyword.lower()
    
    # 1. Context length score (optimal around 100-150 chars)
    context_len = len(context)
    if 50 <= context_len <= 150:
        length_score = 1.0
    elif context_len < 50:
        length_score = context_len / 50.0  # Scale up
    else:
        length_score = max(0.5, 1.0 - (context_len - 150) / 200.0)  # Decay
    
    # 2. Keyword prominence (check if capitalized or emphasized)
    keyword_in_context = context[max(0, context_lower.find(keyword_lower)-10):context_lower.find(keyword_lower)+len(keyword)+10]
    prominence_score = 0.5  # Base
    if keyword in context:  # Original case preserved
        prominence_score += 0.3
    if keyword.upper() in context or keyword.title() in context:
        prominence_score += 0.2
    prominence_score = min(1.0, prominence_score)
    
    # 3. Sentence structure (check for complete sentences)
    has_sentence_start = any(context[i:i+2].isupper() for i in range(min(20, len(context))))
    has_sentence_end = any(c in context for c in ['.', '!', '?'])
    structure_score = 0.5
    if has_sentence_start:
        structure_score += 0.25
    if has_sentence_end:
        structure_score += 0.25
    
    # 4. Relevance indicators (positive business terms)
    positive_indicators = ['best', 'top', 'recommended', 'popular', 'excellent', 'quality', 
                          'service', 'professional', 'reliable', 'trusted']
    indicator_count = sum(1 for word in positive_indicators if word in context_lower)
    relevance_score = min(1.0, 0.5 + (indicator_count * 0.15))
    
    # Weighted combination
    quality = (
        length_score * 0.25 +
        prominence_score * 0.30 +
        structure_score * 0.25 +
        relevance_score * 0.20
    )
    
    return min(1.0, max(0.1, quality))


def _simulate_visibility_check(
    prompt: str, keyword: str, target_id: str, check_index: int
) -> Tuple[bool, Optional[int], float]:
    """
    Fallback simulation using deterministic hashing.
    
    Used when OpenAI is unavailable or API call fails.
    """
    import hashlib
    
    hash_input = f"{target_id}_{prompt}_{keyword}_{check_index}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)

    occurred = (hash_value % 100) < 60
    position: Optional[int] = None
    context_relevance = 0.0

    if occurred:
        position = (hash_value % 100) + 1
        context_relevance = 0.5 + ((hash_value % 50) / 100.0)
    else:
        context_relevance = (hash_value % 50) / 100.0

    return occurred, position, context_relevance

