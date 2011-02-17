"""mooli installer. The Python movie database."""

from setuptools import setup


setup(
    name="mooli",
    description="Movie Database",
    packages=['mooli'],
    requires=[
        'elixir',
        'imdbpy',
        'nose',
        'sqlalchemy',
    ]
)
