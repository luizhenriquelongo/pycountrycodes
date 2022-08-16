import unicodedata


def remove_accents(input_str: str) -> str:
    # Borrowed from https://stackoverflow.com/a/517974/1509718
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
