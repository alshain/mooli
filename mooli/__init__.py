"""Mooli, the movie library."""

from sqlalchemy import create_engine
from mooli.library import Library

def open(path):
    """Open a mooli library at said path."""
    engine = create_engine("sqlite:///%s" % path)
    return Library(engine)
