import webbrowser
import urllib
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import json
import tmdb_config

# you will need to create a tmdb_config file with your own API key
API_KEY = tmdb_config.get_key()
BASE_API_URL = 'https://api.themoviedb.org/3/'

class Movie():
    """This class provides a way to store movie-related information."""

    def __init__(self, options):
        if not options.has_key('title'):
            raise Exception('Title is required')

        # default data to given options
        self.data = options.copy()

        # get movie id from api
        self.data['id'] = self.get_movie_id(options)

        # get trailer from API
        self.data['trailer_id'] = self.get_trailer_url(self.data['id'])

        # get other movie metadata from API
        self.data.update(self.get_movie_data(self.data['id']))

    def get_movie_id(self, options):
        # if there is a year specification, use it,
        year_query = ''
        if (('year' in options) and options['year']):
            year_query = '&year=' + options['year']

        # otherwise default to first search result based on title
        api_url = urljoin(BASE_API_URL, 'search/movie?query=' + options['title'] + '&api_key='+ API_KEY + year_query)  #NOQA
        connection = urllib.urlopen(api_url)
        id = json.loads(connection.read())['results'][0]['id']
        connection.close()
        return id

    def get_movie_data(self, movie_id):
        # get poster image and other related movie data for specified movie
        data_url = urljoin(BASE_API_URL, 'movie/' + str(movie_id) + '?api_key=' + API_KEY)  #NOQA
        connection = urllib.urlopen(data_url)
        data = json.loads(connection.read())
        connection.close()
        return data

    def get_trailer_url(self, movie_id):
        # get trailer data for specified movie
        data_url = urljoin(BASE_API_URL, 'movie/' + str(movie_id) + '/videos?api_key=' + API_KEY)  #NOQA
        connection = urllib.urlopen(data_url)
        results = json.loads(connection.read())['results']
        connection.close()
        return results[0]['key']  # return first result key
