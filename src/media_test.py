import media
import json
from mock import Mock, patch
from nose.tools import *

test_options = { 'title':'Toy Story' }
test_movie = media.Movie(test_options)

@patch('media.urllib.urlopen')
def test_get_movie_id_returns_id(mock_urlopen):
    a = Mock()
    a.read.side_effect = [json.dumps({ 'results': [{ 'id': 2 }] })]
    mock_urlopen.return_value = a
    idValue = test_movie.get_movie_id(test_options)
    assert idValue == 2
