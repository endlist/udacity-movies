import webbrowser

class Movie():

    def __init__(self, options):
        self.title = options['title']
        self.storyline = options['storyline']
        self.trailer_youtube_url = options['trailer_link']
        self.poster_image_url = options['poster_image']

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
