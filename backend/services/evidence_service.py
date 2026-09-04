"""
services/evidence_service.py – Evidence file handling and OCR (mock/fallback).

The real Tesseract/OpenCV OCR implementation will replace _extract_ocr_text()
without changing any routes.  The interface is intentionally minimal.
"""

import os
import logging

logger = logging.getLogger("verilaw")

# ──────────────────────────────────────────────────────────────────────
# OCR  (MOCK – replace internals when Tesseract is available)
# ──────────────────────────────────────────────────────────────────────

_PROPERTY_AGREEMENT_SAMPLE = """PROPERTY SALE AGREEMENT
THIS AGREEMENT is made at New Delhi on this 24th day of July, 2022.
BETWEEN:
Mr. Suresh Kumar, residing at Flat 402, Green Avenue, New Delhi (hereinafter called the 'SELLER')
AND
Mr. Ramesh Singh, residing at House 12, Sector 15, Gurgaon (hereinafter called the 'BUYER')

WHEREAS the Seller is the absolute owner of the residential plot situated at Plot No. 102, Dwarka Sector 4, New Delhi (hereinafter called the 'Property').

NOW IT IS MUTUALLY AGREED AS FOLLOWS:
1. The Seller agrees to sell and the Buyer agrees to purchase the Property for a total consideration of INR 75,00,000 (Seventy-Five Lakhs Rupees).
2. The Buyer has paid an advance amount of INR 10,00,000 (Ten Lakhs Rupees) to the Seller on 24th July, 2022.
3. The balance payment shall be paid by the Buyer on or before 24th July, 2026.
4. The Seller warrants that the Property is free from all encumbrances, liens, or disputes.

IN WITNESS WHEREOF the parties have set their signatures on the day and year first above written.

Witnesses:
1. [Signature] (Copy-Pasted Notary Seal Block)
2. [Blank]
"""


def extract_ocr_text(original_name: str, file_path: str) -> tuple[str, float]:
    """
    Extract text from an uploaded file.

    Returns:
        (ocr_text, confidence)  where confidence is 0.0–100.0

    REAL OCR STUB: Install pytesseract + opencv-python and replace the
    body of this function. Keep the signature unchanged.
    """
    name_lower = original_name.lower()
    if any(kw in name_lower for kw in ("agree", "contract", "rent", "lease")):
        return _PROPERTY_AGREEMENT_SAMPLE, 96.0

    fallback = (
        f"Extracted Text from {original_name}:\n"
        "[Legal Document content matches general civil format. "
        "Biometric signature block identified. "
        "Notary seal matches registered database of 2026.]"
    )
    return fallback, 0.0


def infer_category(original_name: str) -> str:
    """Infer an evidence category from the filename (rule-based fallback)."""
    name_lower = original_name.lower()
    if any(kw in name_lower for kw in ("property", "agree", "land", "plot")):
        return "Property Dispute"
    return "Consumer Complaint"
