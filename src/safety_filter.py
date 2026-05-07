import re


DISCLAIMER = (
    "This tool is for educational analysis only. It does not provide personalized "
    "investment advice, buy/sell recommendations, or price targets."
)

WARNING = (
    "Note: The system is designed for educational analysis only and should not be "
    "interpreted as investment advice."
)

DIRECT_RECOMMENDATION_PATTERNS = [
    r"\byou should buy\b",
    r"\byou should sell\b",
    r"\bstrong buy\b",
    r"\bprice target\b",
    r"\bguaranteed\b",
    r"\brisk-free\b",
]


def detect_direct_recommendation(response: str) -> bool:
    return any(
        re.search(pattern, response, flags=re.IGNORECASE)
        for pattern in DIRECT_RECOMMENDATION_PATTERNS
    )


def soften_recommendation_language(response: str) -> str:
    if detect_direct_recommendation(response) and WARNING not in response:
        return f"{response.rstrip()}\n\n{WARNING}"
    return response


def add_disclaimer(response: str) -> str:
    response = soften_recommendation_language(response)
    if DISCLAIMER in response:
        return response
    return f"{response.rstrip()}\n\n---\n\n{DISCLAIMER}"
