import media
import fresh_tomatoes

movies = [
    media.Movie({
        'title': 'snatch',
        'year': ''
    }),
    media.Movie({
        'title': 'iron Man',
    }),
    media.Movie({
        'title': 'Alice in Wonderland',
        'year': '1951'
    })
]

fresh_tomatoes.open_movies_page(movies)

