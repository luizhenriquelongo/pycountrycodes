import unicodedata


def remove_accents(input_str: str) -> str:
    """
    It takes a string, normalizes it to a form that is easier to work with, and then returns a new string with all the
    accents removed

    Args:
      input_str (str): The string to remove accents from.

    Returns:
      A string with all the accents removed.
    """
    # Borrowed from https://stackoverflow.com/a/517974/1509718
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
