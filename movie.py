class CatMovie:
    id = None
    name = ""
    orig_name = ""
    year = 0
    country = ""
    genre = ""
    length = 0
    rating = ""
    director = ""
    script = ""
    actors = ""
    description = ""
    poster = None

    def get_values_list(self):
        return [self.id, self.name, self.orig_name, self.year, self.country, self.genre, self.length, self.rating, self.director, self.script, self.actors, self.description, self.poster]
