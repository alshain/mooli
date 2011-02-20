"""Movie library."""


import elixir
from sqlalchemy.orm import scoped_session, sessionmaker


from mooli import model as m
from mooli import providers
from mooli import _util as util
from mooli.errors import ProviderError
from mooli.errors import ProviderNotFound
from mooli.errors import MultipleProvidersFound


class Library(object):
    """Movie database."""
    def __init__(self, engine):
        self._session = scoped_session(sessionmaker(autoflush=True,
                                                    bind=engine))
        elixir.setup_all()
        elixir.create_all(engine)
        self.search = Searcher(self)
        self.scrape = Scraper(self)
        self.providers = Providers(self._session)
        self.raw = RawAccess(self._session)
        self.query = self.raw.query

        # Register providers
        self.providers.register(providers.IMDB())


class RawAccess(object):
    """Raw access to the underlying database."""
    def __init__(self, session):
        self.session = session

    def add(self, obj):
        """Add a new object to the database."""
        self.session.add(obj)
        self.session.commit()

    def query(self, *args, **kwargs):
        """Wrapper for the sessions's query."""
        return self.session.query(*args, **kwargs)

    def update(obj):
        """Write changes of an object back to the database."""
        raise NotImplementedError("Cannot update objects yet.")


class Providers(object):
    def __init__(self, session):
        self._session = session
        self.by_url = {}
        self.providers = set()

    def __call__(self):
        """Return all providers.
        >>> import mooli
        >>> l = mooli.open(None)
        >>> l.providers
        <Providers: <None>>

        """
        return self._session.query(m.Provider).all()

    def search(self, title, year):
        """Search for a movie by year and title."""
        raise NotImplementedError

    def register(self, provider):
        """Register a new provider with the collection."""

        # Gracefully abort if provider is already registered.
        # by_urls: url: (in_db, provider)
        if provider in self.providers:
            return

        # Check whether we already have a provider that acts upon one of the
        # urls that I'm trying to register.
        collisions = set(self.by_url.keys()).intersection(set(provider.urls))
        if collisions:
            raise ProviderError("Multiple url handlers found: %s" %
                    collisions)

        # All systems go.

        # Need to check whether something what's in the database that the
        # provider can handle.
        ps_in_db = self._session.query(m.Provider).all()
        found_p_in_db = None

        for p_in_db in ps_in_db:
            urls = [url.url for url in p_in_db.urls]
            # I don't think we should ever get here.
            assert not found_p_in_db, "Multiple providers registered?"
            if any(provider.handles(url) for url in urls):
                # URLs are variations for one logical provider.
                found_p_in_db = p_in_db

        if found_p_in_db:
            # Maybe we changed some supported URLs. Let's rewrite them all.
            # Remove old links from the database first.
            for url in p_in_db.urls:
                self._session.delete(url)
            # Flush! so we don't get errors because of non-unique urls
            self._session.flush()
            # And add new ones.
            p_in_db.urls = [m.ProviderUrl(p_in_db, url)
                            for url in provider.urls]
        else:
            # Didn't find the provider.
            # Let's register the provider in the database then.
            p_in_db = m.Provider(provider.urls)
            self._session.add(p_in_db)
        # Write all changes to db
        self._session.flush()

        # And register it
        for url in provider.urls:
            self.by_url[url] = (p_in_db, provider)
        self.providers.add(provider)

    def __getitem__(self, url):
        return self.by_url[url]

    def __repr__(self):
        reps = [repr(p) for p in self.by_url.iteritems()] or ["<None>"]
        return "<Providers: %s>" % ", ".join(reps)


class Scraper(object):
    """Scrapes the internet for movies from a set of providers."""
    def __init__(self, library):
        self.library = library
        self.providers = []


class Searcher(object):
    """Searches the individual providers for a movie."""
    def __init__(self, library):
        self.library = library

    def __iter__(self):
        """Iterate the search results."""
        raise NotImplementedError

    def search(self, title, year, autoscrape=None):
        """See __call__"""
        self(title, year, autoscrape)

    def __call__(self, title, year=None, autoscrape=None):
        """Performs a search."""
        words = util.split_words(title)
        q = self.library.raw.query(m.Movie).join(m.MovieTitle)
        for word in words:
            # Surround with wildcards
            word = unicode("%%%s%%" % word)
            q = q.filter(m.MovieTitle.title.like(word))
        if year:
            q = q.filter(m.Movie.year == year)
        return q.all()

    def by_identifier(self, provider, identifier):
        for provider in self.library.providers:
            pass

    def scrape(self):
        """Fetch information online for the current search."""
        raise NotImplementedError


class Search(object):
    """Represents an individual search."""
    def guess(self):
        """Try to determine which movie one was looking for."""
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
