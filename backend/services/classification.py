"""
services/classification.py – Keyword-based complaint classifier.

This is a temporary keyword fallback. When ML training is ready, replace
classify_complaint() with a call to the trained TF-IDF + classifier pipeline,
keeping the same function signature and return type.
"""

import re

# ──────────────────────────────────────────────────────────────────────
# KEYWORD MAP  (category → list of keywords)
# ──────────────────────────────────────────────────────────────────────

_KW = {
    "Consumer Complaint":  ["product", "defective", "refund", "seller", "purchase",
                            "ecommerce", "delivery", "quality", "warranty"],
    "Labour Complaint":    ["salary", "employer", "workplace", "job", "harassment",
                            "termination", "wage", "employee", "pf", "esi"],
    "Cyber Crime":         ["online", "fraud", "hack", "phishing", "scam", "cyber",
                            "internet", "password", "otp", "upi", "debit"],
    "Property Dispute":    ["land", "property", "rent", "tenant", "encroachment",
                            "lease", "boundary", "ownership", "plot", "title"],
    "Banking Complaint":   ["bank", "loan", "account", "credit", "debit", "emi",
                            "atm", "transaction", "neft", "rtgs", "ifsc"],
    "Insurance Complaint": ["insurance", "claim", "policy", "premium", "settlement",
                            "coverage", "maturity", "nominee"],
    "Municipal Complaint": ["water", "roads", "garbage", "electricity", "municipality",
                            "drainage", "street", "light", "pothole"],
    "RTI":                 ["rti", "information", "government", "public",
                            "transparency", "records", "right", "cpio"],
    "Women Safety":        ["harassment", "dowry", "domestic", "violence", "women",
                            "safety", "abuse", "stalking", "acid"],
    "Tenant Dispute":      ["rent", "landlord", "tenant", "eviction", "deposit",
                            "lease", "accommodation", "notice"],
}

# ──────────────────────────────────────────────────────────────────────
# DEPARTMENT MAP  (category → department name)
# ──────────────────────────────────────────────────────────────────────

_DEPT_MAP = {
    "Consumer Complaint":  "Consumer Commission",
    "Labour Complaint":    "Labour Department",
    "Cyber Crime":         "Cyber Crime Cell",
    "Property Dispute":    "Land Revenue Department",
    "Banking Complaint":   "Banking Ombudsman",
    "Insurance Complaint": "IRDAI",
    "Municipal Complaint": "Municipal Corporation",
    "RTI":                 "Central Information Commission",
    "Women Safety":        "National Commission for Women",
    "Tenant Dispute":      "District Court",
}


def get_department_for_category(category_name: str) -> str:
    """Return the department name for a given category, or empty string."""
    return _DEPT_MAP.get(category_name, "")


def classify_complaint(text: str) -> tuple[str, float]:
    """
    Classify complaint text using keyword matching.

    Returns:
        (category_name, confidence_percent)

    FUTURE: Replace internals with a trained TF-IDF + classifier model.
    Keep this function signature unchanged so callers don't break.
    """
    words = set(re.findall(r"\b\w+\b", text.lower()))
    scores = {cat: sum(1 for kw in kws if kw in words) for cat, kws in _KW.items()}
    best = max(scores, key=lambda c: scores[c])
    total = sum(scores.values()) or 1
    confidence = round(min((scores[best] / total) * 100, 99.99), 2)
    if scores[best] == 0:
        best, confidence = "Consumer Complaint", 50.0
    return best, confidence
