import imdb

class Imdb(object):
    """Base class for all providers."""
    def __init__(self):
        self.imdb = imdb.IMDb()

    def scrape(self, identifier):
        pass

    def search(self, title, year):
        q = "%s (%s)" % (title, year)
        results = self.imdb.search_movie(q)
        pass

    def handles(self, url):
        valid = [
            'imdb',
            'imdb.com',
            'www.imdb.com'
            ]
        return url in valid
