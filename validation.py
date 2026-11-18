import unicodedata


def validate_text(text: str) -> str | None:
    """Return a rejection reason if text is unsuitable for analysis."""

    if not any(char.isalpha() for char in text):
        return "no_alphabetic_characters"

    if any(
        unicodedata.category(char) == "Cc" and char not in "\n\r\t" for char in text
    ):
        return "invalid_control_characters"

    # Reject excessive repetition of a single character.
    compact = "".join(text.casefold().split())

    if len(compact) >= 20 and len(set(compact)) == 1:
        return "repetitive_text"

    # Reject excessive repetition of a single word.
    words = text.casefold().split()

    if len(words) >= 10 and len(set(words)) == 1:
        return "repetitive_text"

    return None
