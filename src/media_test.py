import media
import json
from mock import Mock, patch
from nose.tools import *

test_options = { 'title':'Toy Story', 'year': '1999' }

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
    mock_get_movie_data.return_value = { 'foo': 'bar', 'baz': 'qux' }
    test_movie = media.Movie(test_options)
    assert_true(test_movie.data.has_key('foo'))
    assert_true(test_movie.data.has_key('baz'))
# end __init__

# get_movie_id
test_movie = media.Movie(test_options)
@patch('media.urllib.urlopen')
def test_get_movie_id_returns_id(mock_urlopen):
    a = Mock()
    a.read.side_effect = [json.dumps({ 'results': [{ 'id': 2 }] })]
    mock_urlopen.return_value = a
    idValue = test_movie.get_movie_id(test_options)
    assert idValue == 2
