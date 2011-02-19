import re


def split_words(text):
    """Split individual words."""
    # Also strip empty elements from beginning and end.
    return [x for x in re.split(r"\W+", text) if x]
