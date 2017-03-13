import webbrowser
import urllib
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import json
import tmdb_config

class Movie():
    """This class provides a way to store movie-related information."""

    # you will need to create a tmdb_config file with your own API key
    API_KEY = tmdb_config.get_key()
    BASE_API_URL = 'https://api.themoviedb.org/3/'

    def __init__(self, options):
        if not options.has_key('title'):
            raise Exception('Title is required')

        # default data to given options
        self.data = options.copy()

        # get movie id from api
        self.data['id'] = self.get_movie_id(options)

        # get trailer from API
        self.data['trailer_id'] = self.get_trailer_url(self.data)

        # get other movie metadata from API
        self.data.update(self.get_movie_data(self.data))

    def get_year_query(self, options):
        year_query = ''
        if (('year' in options) and options['year']):
            year_query = '&year=' + options['year']

        return year_query

    def get_movie_search_query_string(self, options):
        return urljoin(self.BASE_API_URL, 'search/movie?query=' + options['title'] + '&api_key='+ self.API_KEY)  #NOQA

    def get_movie_query_string(self, options):
        return urljoin(self.BASE_API_URL, 'movie/' + str(options['id']) + '?api_key='+ self.API_KEY)  #NOQA

    def get_movie_video_query_string(self, options):
        return urljoin(self.BASE_API_URL, 'movie/' + str(options['id']) + '/videos?api_key='+ self.API_KEY)  #NOQA

    def get_movie_id(self, options):
        # if there is a year specification, use it,
        year_query = self.get_year_query(options)

        # otherwise default to first search result based on title
        api_url = self.get_movie_search_query_string(options) + year_query
        connection = urllib.urlopen(api_url)
        id = json.loads(connection.read())['results'][0]['id']
        connection.close()
        return id

    def get_movie_data(self, options):
        # get poster image and other related movie data for specified movie
        data_url = self.get_movie_query_string(options)
        connection = urllib.urlopen(data_url)
        data = json.loads(connection.read())
        connection.close()
        return data

    def get_trailer_url(self, options):
        # get trailer data for specified movie
        data_url = self.get_movie_video_query_string(options)
        connection = urllib.urlopen(data_url)
        results = json.loads(connection.read())['results']
        connection.close()
        return results[0]['key']  # return first result key
