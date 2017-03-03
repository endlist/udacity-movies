import webbrowser
import urllib
import json
import tmdb_config

API_KEY = tmdb_config.get_key()

class Movie():
    """This class provides a way to store movie-related information."""

    BASE_API_URI = 'https://api.themoviedb.org/3/'

    def __init__(self, options):
        self.data = options.copy()
        self.data['id'] = self.get_movie_id(options)

        # get data from API
        self.data['trailer_id'] = self.get_trailer_url(self.data['id'])
        self.data.update(self.get_movie_data(self.data['id']))

    def get_movie_id(self, options):
        year_query = ''
        if (('year' in options) and options['year']):
            year_query = '&year=' + options['year']

        api_url = self.BASE_API_URI + 'search/movie?query=' + options['title'] + '&api_key='+ API_KEY + year_query
        connection = urllib.urlopen(api_url)

        id = json.loads(connection.read())['results'][0]['id']
        connection.close()
        return id

    def get_movie_data(self, movie_id):
        data_url = self.BASE_API_URI + 'movie/' + str(movie_id) + '?api_key=' + API_KEY
        connection = urllib.urlopen(data_url)
        data = json.loads(connection.read())
        connection.close()
        return data

    def get_trailer_url(self, movie_id):
        data_url = self.BASE_API_URI + 'movie/' + str(movie_id) + '/videos?api_key=' + API_KEY
        connection = urllib.urlopen(data_url)
        data = json.loads(connection.read())['results'][0]['key']
        connection.close()
        return data
