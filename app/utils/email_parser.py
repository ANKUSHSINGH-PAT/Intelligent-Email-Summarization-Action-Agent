import re

def clean_email_text(text: str, max_chars: int = 3000) -> str:
    """
    Clean and normalize email text before sending to LLM.
    """

    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove common reply headers
    reply_patterns = [
        r"On .* wrote:",
        r"From:.*",
        r"Sent:.*",
        r"To:.*",
        r"Subject:.*"
    ]

    for pattern in reply_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Remove email signatures
    signature_patterns = [
        r"--\s.*",
        r"Thanks[\s\S]*",
        r"Regards[\s\S]*",
        r"Best regards[\s\S]*"
    ]

    for pattern in signature_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Final trim
    text = text.strip()

    # Hard truncate to avoid token overflow
    if len(text) > max_chars:
        text = text[:max_chars] + " [truncated]"

    return text
