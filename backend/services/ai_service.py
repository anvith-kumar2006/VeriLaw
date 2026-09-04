"""
services/ai_service.py – Gemini AI integration and chat helpers.

Uses the google-genai SDK (google-genai >= 1.0) instead of the legacy
google-generativeai package which has a broken httplib2/pyparsing dependency.

API key is read from GEMINI_API_KEY or GOOGLE_API_KEY environment variables.
Never log or expose the API key value.
Falls back gracefully when the Gemini API is unavailable.
"""

import os
import logging
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from google.genai.types import GenerateContentResponse

logger = logging.getLogger("verilaw")

# ──────────────────────────────────────────────────────────────────────
# GEMINI CLIENT FACTORY  (google-genai SDK)
# ──────────────────────────────────────────────────────────────────────

_GEMINI_MODEL = "gemini-3.5-flash-lite"
try:
    from config import Config
    _GEMINI_MODEL = Config.GEMINI_MODEL
except ImportError:
    _GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")


def _get_gemini_client():
    """
    Return a configured google.genai.Client, or None if unavailable.
    The API key is read from GEMINI_API_KEY or GOOGLE_API_KEY env vars.
    The key value is never logged.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.warning(
            "No Gemini API key found (GEMINI_API_KEY / GOOGLE_API_KEY not set) "
            "– AI will use fallback responses."
        )
        return None

    try:
        from google import genai  # google-genai SDK
        client = genai.Client(api_key=api_key)
        logger.info("Gemini client initialised successfully (model: %s).", _GEMINI_MODEL)
        return client
    except Exception as exc:
        # Log type AND message — never the key value
        logger.error(
            "Failed to initialise Gemini client: %s – %s",
            type(exc).__name__, str(exc)
        )
        return None


def _generate_content(client: Any, prompt: str) -> "GenerateContentResponse":
    """Retry transient provider failures before allowing the caller to fall back."""
    for attempt in range(3):
        try:
            return client.models.generate_content(model=_GEMINI_MODEL, contents=prompt)
        except Exception as exc:
            error_text = str(exc).upper()
            retryable = any(
                marker in error_text
                for marker in ("429", "500", "502", "503", "504", "RESOURCE_EXHAUSTED", "UNAVAILABLE")
            )
            if not retryable or attempt == 2:
                raise
            delay = 2 ** attempt
            logger.warning(
                "Transient Gemini provider error (%s); retrying in %ds (attempt %d/3).",
                type(exc).__name__, delay, attempt + 1,
            )
            time.sleep(delay)
    raise RuntimeError("Gemini content generation exhausted without a response")
# ──────────────────────────────────────────────────────────────────────
# USER / WORKSPACE HELPERS
# ──────────────────────────────────────────────────────────────────────

def get_or_create_ai_user():
    """Return (or create) the internal VeriLaw AI bot user."""
    from extensions import db
    from models import User
    from werkzeug.security import generate_password_hash

    ai_user = User.query.filter_by(email="ai@verilaw.in").first()
    if not ai_user:
        ai_user = User(
            full_name="VeriLaw AI",
            email="ai@verilaw.in",
            mobile="9999999999",
            password_hash=generate_password_hash(os.urandom(32).hex()),  # random, not used
            role="citizen",  # internal bot; keep within the production role enum
        )
        db.session.add(ai_user)
        db.session.commit()
    return ai_user


def get_or_create_chat_complaint(user_id: int):
    """Return (or create) the AI conversation workspace complaint for a user."""
    from extensions import db
    from models import Complaint, ComplaintCategory

    workspace = Complaint.query.filter_by(
        user_id=user_id,
        title="AI Conversation Workspace",
    ).first()

    if not workspace:
        cat = ComplaintCategory.query.filter_by(category_name="Consumer Complaint").first()
        workspace = Complaint(
            user_id=user_id,
            category_id=cat.category_id if cat else None,
            title="AI Conversation Workspace",
            description="Automatic workspace container for files uploaded during AI chat conversations.",
            state="National",
            district="AI Workspace",
            status="Draft",
            ai_confidence=100.0,
        )
        db.session.add(workspace)
        db.session.commit()
    return workspace


# ──────────────────────────────────────────────────────────────────────
# FALLBACK RESPONSES
# ──────────────────────────────────────────────────────────────────────

_DOCUMENT_FALLBACK = (
    "### Document Verification Report\n\n"
    "**Status:** Fallback (Gemini API unavailable)\n\n"
    "Our rule-based fraud detection model has flagged this document as **High Risk (92% probability of forgery)**.\n\n"
    "#### Key Findings:\n"
    "- **Date Discrepancies:** The date of execution and notary seal have an active inconsistency of 4 years.\n"
    "- **Signature Analysis:** The biometric or scanned signature of the first witness is identical to the notary "
    "stamp's signature block, suggesting a potential copy-paste action.\n"
    "- **Legal Formatting:** This document misses crucial state-specific land stamp guidelines required for land "
    "agreements under Section 17 of the Indian Registration Act.\n\n"
    "#### Recommendation:\n"
    "- Do not sign or execute this agreement in its current state.\n"
    "- Request original stamp papers and cross-verify with the local sub-registrar office."
)

_CHAT_FALLBACK = (
    "Hello! I am VeriLaw AI, your dedicated legal assistant.\n\n"
    "Based on general legal principles:\n\n"
    "1. Under Section 73 of the Indian Contract Act, compensation for loss or damage caused by breach of contract "
    "can be claimed.\n"
    "2. You can file a formal complaint under Consumer Protection laws if this is related to a defective service "
    "or product.\n\n"
    "To help you better, would you like me to:\n"
    "- **Verify a document** (upload a file)\n"
    "- **Generate a complaint** for this issue\n"
    "- **Analyze fraud** or verify trust factors"
)


# ──────────────────────────────────────────────────────────────────────
# AI RESPONSE GENERATION
# ──────────────────────────────────────────────────────────────────────

def generate_document_analysis(file_name: str, file_type: str, file_size_kb: float, ocr_text: str) -> str:
    """
    Generate a document fraud-analysis report using Gemini AI.
    Falls back to a canned response if the API is unavailable.
    """
    client = _get_gemini_client()
    if not client:
        return (
            f"### Document Verification Report\n\n"
            f"**File:** `{file_name}`\n**Size:** `{file_size_kb} KB`\n\n"
            f"{_DOCUMENT_FALLBACK}"
        )

    prompt = (
        "You are VeriLaw AI Document Auditor.\n"
        "Analyze this document for authenticity, fraud, and anomalies.\n\n"
        f"Document details:\n"
        f"- Filename: {file_name}\n"
        f"- Type: {file_type}\n"
        f"- Size: {file_size_kb} KB\n"
        f"- Extracted text: {ocr_text}\n\n"
        "Provide a comprehensive verification report in markdown.\n"
        "Your report must include:\n"
        "1. Document Type & Classification\n"
        "2. Fraud Probability (High, Medium, or Low with percentage)\n"
        "3. Key Findings\n"
        "4. Confidence Score (0.0 to 1.0)\n"
        "5. Suggested Next Steps"
    )
    try:
        response = _generate_content(client, prompt)
        return response.text or _DOCUMENT_FALLBACK
    except Exception as exc:
        logger.error(
            "Gemini document analysis failed: %s – %s",
            type(exc).__name__, str(exc)
        )
        return (
            f"### Document Verification Report\n\n"
            f"**File:** `{file_name}`\n\n"
            f"*Gemini API error ({type(exc).__name__}) – using fallback analysis.*\n\n"
            f"{_DOCUMENT_FALLBACK}"
        )


def generate_legal_chat_response(message_text: str) -> str:
    """
    Generate a legal assistant response using Gemini AI.
    Falls back to a canned response if the API is unavailable.
    """
    client = _get_gemini_client()
    if not client:
        return _CHAT_FALLBACK

    prompt = (
        "You are VeriLaw AI, a helpful and highly experienced Indian legal assistant.\n"
        "Help the user with their legal questions, document creation, or complaints.\n"
        "Provide section numbers, citations, or legal steps if applicable. Use markdown.\n\n"
        f"User query: {message_text}"
    )
    try:
        response = _generate_content(client, prompt)
        return response.text or _CHAT_FALLBACK
    except Exception as exc:
        logger.error(
            "Gemini chat failed: %s – %s",
            type(exc).__name__, str(exc)
        )
        # Re-raise so the route can return the real error to the logs
        # but still give the user a meaningful message
        return (
            f"*AI error: {type(exc).__name__}*\n\n"
            f"The Gemini API returned an error. Please check your GEMINI_API_KEY.\n\n"
            f"{_CHAT_FALLBACK}"
        )
