"""
extract_disclosure.py
Part 3B - Structured disclosure extraction
MOCK_LLM baseline: keyword/regex rule-based extraction, no LLM call.
"""

from disclosure_snippets import DISCLOSURE_SNIPPETS

# Keyword sets driving the rule-based classification
LITIGATION_KEYWORDS = ["litigation", "lawsuit", "legal matter"]
REGULATORY_KEYWORDS = ["regulatory", "regulator", "compliance", "data-localization"]
CUSTOMER_CONCENTRATION_KEYWORDS = ["customer concentration", "top three customers", "percent of", "% of"]

HEDGING_KEYWORDS = ["assuming", "cautiously", "visibility"]
CONFIDENT_KEYWORDS = ["confident", "approved"]


def extract_signals(snippet: str) -> dict:
    """
    Rule-based extraction (MOCK_LLM baseline).
    Returns: {"risk_flags": [...], "hedging_detected": bool,
              "sentiment": "confident" | "cautious" | "neutral"}
    """
    text_lower = snippet.lower()

    risk_flags = []
    if any(kw in text_lower for kw in LITIGATION_KEYWORDS):
        risk_flags.append("litigation")
    if any(kw in text_lower for kw in REGULATORY_KEYWORDS):
        risk_flags.append("regulatory")
    if any(kw in text_lower for kw in CUSTOMER_CONCENTRATION_KEYWORDS):
        risk_flags.append("customer_concentration")

    hedging_detected = any(kw in text_lower for kw in HEDGING_KEYWORDS)

    if any(kw in text_lower for kw in CONFIDENT_KEYWORDS):
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment,
    }


if __name__ == "__main__":
    print("=== Paytm Disclosure Signal Extraction (MOCK_LLM mode) ===\n")
    for snippet in DISCLOSURE_SNIPPETS:
        result = extract_signals(snippet)
        print(f"Snippet: {snippet}")
        print(f"  Risk Flags: {result['risk_flags']}")
        print(f"  Hedging Detected: {result['hedging_detected']}")
        print(f"  Sentiment: {result['sentiment']}")
        print()