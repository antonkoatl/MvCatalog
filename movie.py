from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget, QWidget
import data.design_main

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


    def __init__(self, item=None):
        if item is None: return
        self.id = item[10]
        self.name = item[11] if item[11] is not None else item[12]
        self.orig_name = item[12]
        self.year = int(item[13])
        self.country = item[14]
        self.genre = item[15]
        self.length = int(item[16])
        self.rating = item[17]
        self.director = item[18]
        self.script = item[19]
        self.actors = item[20]
        self.description = item[21]
        self.poster = item[22]

    def get_values_list(self):
        return [self.id, self.name, self.orig_name, self.year, self.country, self.genre, self.length, self.rating, self.director, self.script, self.actors, self.description, self.poster]

    def fill_widget(self, form: data.design_main.Ui_MainWindow):

        pixmap = QPixmap()
        pixmap.loadFromData(self.poster)
        pixmap = pixmap.scaled(form.label.width(), form.label.height(), Qt.KeepAspectRatio)
        form.label.setPixmap(pixmap)

        form.label_3.setText(self.name)
        form.label_7.setText(self.orig_name)
        form.label_9.setText(str(self.year))
        form.label_11.setText(self.country)
        form.label_13.setText(self.genre.replace(",", ", "))
        form.label_15.setText(str(self.length))
        form.label_17.setText(self.rating)
        form.label_19.setText(self.director)
        form.label_21.setText(self.script)
        form.label_5.setText(self.actors)

        form.plainTextEdit.setPlainText(self.description)
