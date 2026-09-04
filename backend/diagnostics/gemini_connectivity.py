"""Minimal live Gemini connectivity diagnostic.

Run from the repository root with: python backend/diagnostics/gemini_connectivity.py
The API key is never printed.
"""

import importlib.metadata
import os
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from config import Config
from services import ai_service


def _redact(message: str) -> str:
    for variable_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        secret = os.environ.get(variable_name)
        if secret:
            message = message.replace(secret, "[REDACTED]")
    return message


def main() -> int:
    key_present = bool(
        os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    )
    configured_model = ai_service._GEMINI_MODEL
    print(f"key present: {'YES' if key_present else 'NO'}")
    print(f"model configured: {configured_model}")
    print(f"SDK version: {importlib.metadata.version('google-genai')}")

    client = ai_service._get_gemini_client()
    if not client:
        print("API request: FAIL")
        print("HTTP/API error category: client initialization")
        print("fallback activated: YES")
        return 1

    try:
        response = client.models.generate_content(
            model=configured_model,
            contents="Reply with exactly: GEMINI_CONNECTIVITY_OK",
        )
        success = bool(getattr(response, "text", None))
        print(f"API request: {'SUCCESS' if success else 'FAIL'}")
        print("HTTP/API error category: none" if success else "HTTP/API error category: empty response")
        print(f"fallback activated: {'NO' if success else 'YES'}")
        return 0 if success else 1
    except Exception as exc:
        print("API request: FAIL")
        print(f"HTTP/API error category: {type(exc).__name__}")
        print(f"error detail: {_redact(str(exc))[:700]}")
        print("fallback activated: YES")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
