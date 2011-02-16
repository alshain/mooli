"""Movie library."""

from sqlalchemy.orm import scoped_session, sessionmaker
from mooli import model
from mooli import model as m


def connect(engine=None):
    return Library(engine)


class Library(object):
    """Movie database."""
    def __init__(self, engine=None):
        if not model.metadata.bind:
            model.metadata.bind = engine or "sqlite:///:memory:"
        self._session = scoped_session(sessionmaker(autoflush=True,
                                                    bind=engine))
        model.setup_all()
        model.create_all()
        pass

    def providers(self):
        """Return all providers.
        >>> from mooli import library
        >>> from mooli import model
        >>> l = library.connect()
        >>> l.add(model.Provider("imdb.com"))
        >>> l.providers()  #doctest:+ELLIPSIS
        [<mooli.model.Provider object at ...>]

        """
        """Return a list of all providers."""
        return self._session.query(m.Provider).all()

    def update(obj):
        """Write changes of an object back to the database."""
        raise NotImplementedError("Cannot update objects yet.")

    def add(self, obj):
        """Add a new object to the database."""
        self._session.add(obj)
        self._session.commit()

    def search(movie, year=None, autoscrape=False):
        """Search the library and optionally scrape if no results found."""
        raise NotImplementedError("Cannot search yet")
