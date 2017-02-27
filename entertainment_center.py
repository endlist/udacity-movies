import media
import fresh_tomatoes

toy_story = media.Movie({
    'title': 'Toy Story',
    'storyline': 'Toys',
    'poster_image': 'https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg',
    'trailer_link': 'https://www.youtube.com/watch?v=vwyZH85NQC4'
})

movies = [toy_story]
fresh_tomatoes.open_movies_page(movies)

