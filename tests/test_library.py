from nose.tools import eq_
from mooli import Library
from mooli import model

def test_scrape():
    model.metadata.bind = None
    library = Library()
    library.scrape("The Matrix", 1999)

def test_matrix():
    print "Instantiatig Library."
    model.metadata.bind = None
    library = Library()
    print "Search by IMDB ID"
    results = library.search("The Matrix", autoscrape=True)
    matrix = results.guess()
    eq_(matrix.title, "The Matrix")
    eq_(matrix.year, 1999)

