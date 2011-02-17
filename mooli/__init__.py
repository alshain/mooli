"""Mooli, the movie library."""

from sqlalchemy import create_engine
from mooli.library import Library


def open(path=None):
    """Open a mooli library at said path."""
    if path:
        engine = create_engine("sqlite:///%s" % path)
    else:
        engine = create_engine("sqlite:///:memory:")
    return connect(engine)


def connect(engine):
    """Connect library to an open database."""
    return Library(engine)
