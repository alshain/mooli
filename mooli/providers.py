import traceback


import imdb


class IMDB(object):
    """Base class for all providers."""
    def __init__(self):
        self.imdb = imdb.IMDb()
        self.urls = [
            'imdb',
            'imdb.com',
            'www.imdb.com'
            ]

    def search(self, title, year):
        # Study: How do I best search on IMDB if I have a movie and the year?
        # It turns out, searching for "The Matrix 1999" produces 20! results
        # whereas searching for "The Matrix (1999)" produces only a single
        # result, and it's correct even.
        q = "%s (%s)" % (title, year)
        results = self.imdb.search_movie(q)
        return [self._process_result(x) for x in results]

    def _process_result(self, data):
        # Structure of the result is as follows:
        # * identifier
        # * title
        # * sort title
        # * titles (title, description)
        # * year
        result = {}
        result["title"] = data["title"]

        # What does all the smart stuff do?
        # consider this: "Die Hard (1988)
        #   >>> m["canonical title"]
        #   u'Hard, Die'
        #   >>> m["smart canonical title"]
        #   u'Die Hard'
        # IMDB apparently uses a very primitve approach and thinks it's a
        # german article. All hail imdbpy magic!
        result["sort"] = data["smart canonical title"]
        result["year"] = data["year"]
        result["id"] = data.movieID
        result["titles"] = []

        try:
            akas = data["akas"]
        except KeyError:
            aka_data = self.imdb.get_movie_akas(result["id"])["data"]
            try:
                akas = aka_data["akas from release info"]
            except KeyError:
                traceback.print_exc()

        for aka in akas:
            aka, description = aka.split("::")
            result["titles"].append((aka, description))
        return result

    def handles(self, url):
        return url in self.urls
