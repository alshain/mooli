from nose.tools import eq_, ok_, raises
from minimock import Mock


import mooli
from mooli.library import MultipleProvidersFound


def test_scrape():
    model.metadata.bind = None
    library = Library()
    library.scrape("The Matrix", 1999)

def test_matrix():
    print "Instantiatig Library."
    library = mooli.open()
    print "Search by name, and scrape."
    results = library.search("The Matrix", 1999, autoscrape=True)
    matrix = results.guess()
    eq_(matrix.title, "The Matrix")
    eq_(matrix.year, 1999)


def test_providers():
    lib = mooli.open()
    mock_imdb = Mock("imdb")
    mock_imdb.handles = Mock("handles", returns=True)
    mock_tmdb = Mock("tmdb")
    mock_tmdb.handles = Mock("handles", returns=False)
    lib.providers.register(mock_imdb)
    ok_(lib.providers["imdb.com"] is mock_imdb, "Should be mock_imdb.")

@raises(MultipleProvidersFound)
def test_provider_url_clash():
    lib = mooli.open()
    mock_imdb = Mock("imdb")
    mock_tmdb = Mock("tmdb")
    # Let both providers handle all URLs.
    mock_imdb.handles = Mock("imdb.handles", returns=True)
    # Register both providers
    mock_tmdb.handles = Mock("tmdb.handles", returns=True)
    lib.providers.register(mock_imdb)
    lib.providers.register(mock_tmdb)
    # This has throw an exception.
    fails = lib.providers["imdb.com"]
