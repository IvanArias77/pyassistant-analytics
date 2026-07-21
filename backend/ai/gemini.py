"""
Google Gemini AI integration using the new google-genai SDK.

This module uses the official google-genai package (successor to google-generativeai).
Documentation: https://googleapis.github.io/python-genai/
"""
from google import genai
from google.genai import types
from config import settings
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def _is_valid_api_key(key: str) -> bool:
    """
    Validate API key format.

    Gemini API keys typically start with 'AIza' and are ~39 characters long.
    """
    if not key:
        return False
    if key == "your_gemini_api_key_here":
        return False
    # Real Gemini keys start with "AIza" and are 39 chars
    if not re.match(r'^AIza[A-Za-z0-9_-]{35,}$', key):
        logger.warning("⚠️ GEMINI_API_KEY format looks invalid (should start with 'AIza')")
        # Don't fail - let the API call decide, but warn
    return True


# Configure Gemini with the new SDK
if settings.GEMINI_API_KEY and _is_valid_api_key(settings.GEMINI_API_KEY):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        MODEL_ID = "gemini-2.0-flash-exp"
        AI_ENABLED = True
        logger.info("✅ Gemini AI configured successfully (google-genai SDK)")
    except Exception as e:
        logger.error(f"❌ Failed to configure Gemini: {e}")
        AI_ENABLED = False
else:
    AI_ENABLED = False
    logger.warning("⚠️ GEMINI_API_KEY not configured - AI features disabled")


async def generate_insights(activities_data: dict) -> str:
    """
    Generate AI insights from activity data.

    Args:
        activities_data: Dict with summary, by_category, daily metrics

    Returns:
        AI-generated analysis in natural language
    """
    if not AI_ENABLED:
        return "⚠️ AI features are disabled. Please configure GEMINI_API_KEY in your .env file to enable insights."

    prompt = f"""You are a productivity analyst AI. Analyze the following activity tracking data and provide actionable insights in Spanish.

Data:
{activities_data}

Provide a concise analysis (max 200 words) covering:
1. 📊 Main patterns observed
2. ✅ What's working well
3. ⚠️ Areas for improvement
4. 💡 2-3 specific recommendations

Be direct, use emojis for readability, and focus on actionable advice."""

    try:
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"❌ Error generating insights: {str(e)}"


async def answer_question(question: str, activities_data: dict) -> str:
    """
    Answer a natural language question about activity data.

    Args:
        question: User's question in natural language (Spanish or English)
        activities_data: Context data about activities

    Returns:
        AI-generated answer
    """
    if not AI_ENABLED:
        return "⚠️ AI features are disabled. Please configure GEMINI_API_KEY in your .env file."

    prompt = f"""You are a personal productivity assistant. Answer the following question about the user's activity data.

User's question: "{question}"

Activity data context:
{activities_data}

Provide a clear, direct answer in the SAME language as the question. Use specific numbers from the data when possible. Be conversational but concise (max 150 words)."""

    try:
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"❌ Error: {str(e)}"


def is_ai_enabled() -> bool:
    """Check if AI features are available."""
    return AI_ENABLED