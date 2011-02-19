"""Movie library."""


import elixir
from sqlalchemy.orm import scoped_session, sessionmaker


from mooli.exceptions import MooliError
from mooli import model as m
from mooli import _util as util


class ProviderError(MooliError):
    pass


class ProviderNotFound(ProviderError):
    pass


class MultipleProvidersFound(ProviderError):
    pass


class Library(object):
    """Movie database."""
    def __init__(self, engine):
        self._session = scoped_session(sessionmaker(autoflush=True,
                                                    bind=engine))
        elixir.setup_all()
        elixir.create_all(engine)
        self.search = Search(self)
        self.scrape = Scraper(self)
        self.providers = Providers(self._session)


    def update(obj):
        """Write changes of an object back to the database."""
        raise NotImplementedError("Cannot update objects yet.")

    def add(self, obj):
        """Add a new object to the database."""
        self._session.add(obj)
        self._session.commit()


class Providers(object):
    def __init__(self, session):
        self._session = session
        self.providers = set()

    def __call__(self):
        """Return all providers.
        >>> import mooli
        >>> l = mooli.open(None)
        >>> l.providers  #doctest:+ELLIPSIS
        <Providers: <None>>

        """
        return self._session.query(m.Provider).all()

    def add(self, urls):
        """Register a new movie provider."""
        if isinstance(urls, str):
            urls = [urls]


    def by_url(self, url, autocreate=False):
        """Return by URL.

        >>> import mooli
        >>> l = mooli.open(None)
        >>> l.providers.by_url("imdb.com")  #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ProviderNotFound: No provider handles that url.

        """
        # q = self.session.query(model.ProviderUrl)
        # return q.filter(model.ProviderUrl.url == url).one().provider
        filtered = filter(lambda p: p.handles(url), self.providers)
        if len(filtered) == 1:
            return filtered[0]
        elif len(filtered) > 1:
            # Unpredictable behaviour would occur.
            raise MultipleProvidersFound("Multiple providers found.")
        else:
            raise ProviderNotFound("No provider handles that url.")

    def __getitem__(self, url):
        return self.by_url(url)

    def register(self, provider):
        """Register a new provider with the collection."""
        self.providers.add(provider)

    def __repr__(self):
        reps = [repr(p) for p in self.providers] or ["<None>"]
        return "<Providers: %s>" % ", ".join(reps)


class Scraper(object):
    """Scrapes the internet for movies from a set of providers."""
    def __init__(self, library):
        self.library = library
        self.providers = []


class Search(object):
    """Searches the individual providers for a movie."""
    def __init__(self, library):
        self.library = library

    def __iter__(self):
        """Iterate the search results."""
        raise NotImplementedError

    def search(self, title, year, autoscrape=None):
        """See __call__"""
        self(title, year, autoscrape)

    def __call__(self, title, year, autoscrape=None):
        """Performs a search."""
        # Split words

    def by_identifier(self, provider, identifier):
        for provider in self.library.providers:
            pass

    def guess(self):
        """Try to determine which movie one was looking for."""
        raise NotImplementedError

    def scrape(self):
        """Fetch information online for the current search."""
        raise NotImplementedError


class SearchResult(object):
    """Represents a movie result."""
    def __init__(self, title, year):
        self.title = title
        self.year = int(year)
        self.aka = []

    def rate(self, title, year):
        # Make it a float, so divisions do what we want.
        score = 0.0
        # Year punishment
        if year != self.year:
            decades = abs(self.year - year) // 10
            score -= 0.05 * (decades + 1)
