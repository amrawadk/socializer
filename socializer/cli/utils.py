import pyarabic.araby as araby


def _is_arabic(name: str) -> bool:
    return all((c in araby.LETTERS for c in name.replace(" ", "")))
