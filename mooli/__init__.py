"""Mooli, the movie library."""

from sqlalchemy import create_engine
from mooli.library import Library


class MooliError(Exception):
    pass


def open(path):
    """Open a mooli library at said path."""
    engine = create_engine("sqlite:///%s" % path)
    return connect(engine)

def connect(engine):
    return Library(engine)
