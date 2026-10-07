def normalize_title(raw: str) -> str:
    """Нормалізує назву: прибирає зайві пробіли та переводить у нижній регістр."""
    return " ".join(raw.split()).lower()
