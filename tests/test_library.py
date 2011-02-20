from nose.tools import eq_, ok_, raises
from minimock import Mock


import mooli
from mooli import model as m
from mooli.library import MultipleProvidersFound


def test_matrix():
    print "Instantiatig Library."
    library = mooli.open()
    print "Search by name, and scrape."
    results = library.search("The Matrix", 1999, autoscrape=True)
    matrix = results.guess()
    eq_(matrix.title, "The Matrix")
    eq_(matrix.year, 1999)


def test_provider_by_url():
    lib = mooli.open()
    in_db, imdb = lib.providers["imdb.com"]
    ok_(isinstance(in_db, m.Provider), "Should be Provider model.")
    ok_(isinstance(imdb, mooli.providers.IMDB), "Should be Provider model.")
    eq_((in_db, imdb), lib.providers["imdb"], "Multiple urls don't work.")

def test_provider_identify_with_db():
    lib = mooli.open()
    in_db, imdb = lib.providers["imdb.com"]
    # Pretend we have no registerd providers, but one in the database
    # We do that by clearing our registry which is in by_url
    lib.providers.by_url = {}
    lib.providers.register(imdb)
    eq_((in_db, imdb),  lib.providers["imdb.com"])

def test_search():
    lib = mooli.open()
    matrix = mooli.model.Movie("The Matrix", 1999)
    lib._session.add(matrix)
    lib._session.flush()
    ok_(len(lib.search("The Matrix")) == 1, "Expected one result.")
    ok_(len(lib.search("The Matrix", 1999)) == 1, "Expected one result.")
    ok_(len(lib.search("The Matrix", 2000)) == 0, "Exoected no results.")
    ok_(len(lib.search("Matrix")) == 1, "Partial title failed.")
    ok_(len(lib.search("rix")) == 1, "Partial word failed.")
