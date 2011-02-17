import elixir


# We would like to be able to create this schema in a specific database at
# will, so we can test it easily.
# Make elixir not bind to any session to make this possible.
#
# http://elixir.ematia.de/trac/wiki/Recipes/MultipleDatabasesOneMetadata
__session__ = None


class Language(elixir.Entity):
    name = elixir.OneToMany("LanguageName")


class LanguageName(elixir.Entity):
    translation_id = elixir.Field(elixir.Integer, primary_key=True)
    language = elixir.ManyToOne('Language', primary_key=True)
    text = elixir.Field(elixir.Unicode(20), unique=True)


class Provider(elixir.Entity):
    url = elixir.Field(elixir.String(20), required=True, unique=True)

    def __init__(self, url):
        self.url = url


class ExternalMovieId(elixir.Entity):
    provider = elixir.ManyToOne('Provider')
    value = elixir.Field(elixir.Unicode(40))
    movie = elixir.ManyToOne('Movie')
    # such as IMDB's, maybe some use text -> long


class MovieTitle(elixir.Entity):
    language = elixir.ManyToOne('Language')
    movie = elixir.ManyToOne('Movie')
    title = elixir.Field(elixir.UnicodeText)

    def __init__(self, title, movie=None):
        self.title = unicode(title)
        self.movie = movie

class Movie(elixir.Entity):
    titles = elixir.OneToMany('MovieTitle', lazy=False)
    plot = elixir.Field(elixir.UnicodeText)
    year = elixir.Field(elixir.Integer)
    tagline = elixir.Field(elixir.UnicodeText(255))
    genres = elixir.ManyToMany('Genre')
    identifiers = elixir.OneToMany('ExternalMovieId')
    characters = elixir.ManyToMany('Character')
    rating = elixir.OneToOne('Rating')

    def __init__(self, title, year):
        title = unicode(title)
        self.titles.append(MovieTitle(title))


class Character(elixir.Entity):
    names = elixir.OneToMany('CharacterName')
    movies = elixir.ManyToMany('Movie')


class CharacterName(elixir.Entity):
    language = elixir.ManyToOne('Language')
    character = elixir.ManyToOne('Character')


class AssociatedPeople(elixir.Entity):
    directors = elixir.ManyToMany('Person')
    screenwriters = elixir.ManyToMany('Person')
    actors = elixir.ManyToMany('Person')


class AspectRatio(elixir.Entity):
    name = elixir.Field(elixir.Unicode(20), unique=True)
    ratio = elixir.Field(elixir.Float)
    movies = elixir.ManyToMany('Movie')
    # The Dark Knight has multiple...


class Specification(elixir.Entity):
    language = elixir.ManyToOne('Language')
    color = elixir.Field(elixir.Boolean)


class Genre(elixir.Entity):
    name = elixir.Field(elixir.UnicodeText(255))


class Person(elixir.Entity):
    name = elixir.Field(elixir.UnicodeText(50))
    birthday = elixir.Field(elixir.Date)
    identifiers = elixir.OneToMany('ExternalPersonId')


class ExternalPersonId(elixir.Entity):
    provider = elixir.ManyToOne('Provider')
    value = elixir.Field(elixir.Unicode(40))
    person = elixir.ManyToOne('Person')
    # such as IMDB's, maybe some use text -> long


class Rating(elixir.Entity):
    """Score of a movie as users have voted."""
    name = elixir.Field(elixir.UnicodeText(40))
    rating = elixir.Field(elixir.Float)
    # elixir.OneToOne must have a elixir.ManyToOne as inverse
    movie = elixir.ManyToOne('Movie')
    votes = elixir.Field(elixir.Integer)

    def __cmp__(self, other):
        if self.rating < other.rating:
            return -1
        elif self.rating > other.rating:
            return 1
        else:
            return 0


class AgeRating(elixir.Entity):
    """MPAA rating."""
    name = elixir.Field(elixir.UnicodeText(40))
    position = elixir.Field(elixir.Float)
    movies = elixir.ManyToMany('Movie')

    def __cmp__(self, other):
        if self.position < other.position:
            return -1
        elif self.position > other.position:
            return 1
        else:
            return 0
