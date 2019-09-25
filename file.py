class CatFile:
    id = None
    movie_id = -1
    name = ""
    size = ""
    resolution = ""
    codec = ""
    bitrate = 0
    length = 0
    audio = ""
    subtitles = ""

    def get_values_list(self):
        return [self.id, self.movie_id, self.name, self.size, self.resolution, self.codec, self.bitrate, self.length, self.audio, self.subtitles]
