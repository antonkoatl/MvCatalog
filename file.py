import data.design_main

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

    def __init__(self, item):
        self.id = item[0]
        self.movie_id = item[1]
        self.name = item[2]
        self.size = item[3]
        self.resolution = item[4]
        self.codec = item[5]
        self.bitrate = int(item[6])
        self.length = int(item[7])
        self.audio = item[8]
        self.subtitles = item[9]

    def get_values_list(self):
        return [self.id, self.movie_id, self.name, self.size, self.resolution, self.codec, self.bitrate, self.length, self.audio, self.subtitles]

    def fill_widget(self, form: data.design_main.Ui_MainWindow):
        form.tableWidget.item(0, 0).setText(self.name)
        form.tableWidget.item(1, 0).setText(self.size)
        form.tableWidget.item(2, 0).setText(self.resolution)
        form.tableWidget.item(3, 0).setText(self.codec)
        form.tableWidget.item(4, 0).setText(str(self.bitrate))
        form.tableWidget.item(5, 0).setText(str(self.length))
        form.tableWidget.item(6, 0).setText(self.audio)
        form.tableWidget.item(7, 0).setText(self.subtitles)


