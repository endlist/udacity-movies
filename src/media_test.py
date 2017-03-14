import media
import json
from mock import Mock, patch
from nose.tools import eq_, assert_true, assert_raises
import urllib
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

test_options = {
    'title': 'Toy Story',
    'year': '1999'
    }


# __init__
def test_init_fails_with_no_title_option():
    with assert_raises(Exception) as context:
        media.Movie({})

    assert_true('Title is required' in context.exception)


def test_init_succeeds_with_options():
    try:
        media.Movie(test_options)
    except:
        raise AssertionError('valid options should succeed')


def test_init_sets_self_data():
    test_movie = media.Movie(test_options)
    assert_true(test_movie.data is not None)


def test_init_sets_self_data_title():
    test_movie = media.Movie(test_options)
    assert_true(test_movie.data['title'] is not None)


def test_init_sets_self_data_id():
    test_movie = media.Movie(test_options)
    assert_true(test_movie.data['id'] is not None)


def test_init_sets_self_data_trailer_id():
    test_movie = media.Movie(test_options)
    assert_true(test_movie.data['trailer_id'] is not None)


@patch('media.Movie.get_movie_data')
def test_init_sets_self_data_metadata_from_api(mock_get_movie_data):
    mock_get_movie_data.return_value = {'foo': 'bar', 'baz': 'qux'}
    test_movie = media.Movie(test_options)
    assert_true('foo' in test_movie.data)
    assert_true('baz' in test_movie.data)
# end __init__


# get_year_query
def test_get_year_query_uses_year_if_provided():
    test_movie = media.Movie(test_options)
    eq_(test_movie.get_year_query({'year': '2000'}), '&year=2000')


def test_get_year_query_returns_empty_if_no_year():
    test_movie = media.Movie(test_options)
    eq_(test_movie.get_year_query({}), '')
# end get_year_query


# get_movie_search_query_string
def test_get_movie_search_query_returns_query_with_title():
    test_movie = media.Movie(test_options)
    test_movie.BASE_API_URL = 'base_url'
    test_movie.API_KEY = 'newkey'
    movie_title = 'something'
    movie_options = {'title': movie_title}
    api_query_string = urljoin(test_movie.BASE_API_URL, 'search/movie?query=' + movie_title + '&api_key=' + test_movie.API_KEY)  # NOQA

    eq_(
        test_movie.get_movie_search_query_string(movie_options),
        api_query_string
    )
# end get_movie_search_query_string


# get_movie_query_string
def test_get_movie_query_returns_query_with_id():
    test_movie = media.Movie(test_options)
    test_movie.BASE_API_URL = 'base_url'
    test_movie.API_KEY = 'newkey'
    movie_id = 12
    movie_options = {'id': movie_id}
    api_query_string = urljoin(test_movie.BASE_API_URL, 'movie/' + str(movie_id) + '?api_key=' + test_movie.API_KEY)  # NOQA

    eq_(test_movie.get_movie_query_string(movie_options), api_query_string)
# end get_movie_query_string


# get_movie_video_query_string
def test_get_movie_video_query_returns_query_with_id():
    test_movie = media.Movie(test_options)
    test_movie.BASE_API_URL = 'base_url'
    test_movie.API_KEY = 'newkey'
    movie_id = 12
    movie_options = {'id': movie_id}
    api_query_string = urljoin(test_movie.BASE_API_URL, 'movie/' + str(movie_id) + '/videos?api_key=' + test_movie.API_KEY)  # NOQA

    eq_(
        test_movie.get_movie_video_query_string(movie_options),
        api_query_string
    )
# end get_movie_video_query_string


# TODO: make this test_movie context-specific only for following tests
test_movie = media.Movie(test_options)


# get_movie_id
@patch('media.urllib.urlopen')
def test_get_movie_id_returns_id(mock_urlopen):
    a = Mock()
    a.read.side_effect = [json.dumps({'results': [{'id': 2}]})]
    mock_urlopen.return_value = a
    id_value = test_movie.get_movie_id(test_options)
    assert id_value == 2
# end get_movie_id


# get_movie_data
@patch('media.urllib.urlopen')
def test_get_movie_data_returns_data(mock_urlopen):
    mock_response = {'nothing': [{'really': 'matters'}]}
    a = Mock()
    a.read.side_effect = [json.dumps(mock_response)]
    mock_urlopen.return_value = a
    test_options['id'] = 5
    response_value = test_movie.get_movie_data(test_options)
    eq_(response_value, mock_response)
# end get_movie_data


# get_trailer_url
@patch('media.urllib.urlopen')
def test_get_trailer_url_returns_url(mock_urlopen):
    mock_response = 'newurl'
    a = Mock()
    a.read.side_effect = [json.dumps({'results': [{'key': mock_response}]})]
    mock_urlopen.return_value = a
    test_options['id'] = 5
    response_value = test_movie.get_trailer_url(test_options)
    eq_(response_value, mock_response)
# end get_trailer_url

