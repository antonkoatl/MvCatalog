from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import data.design_dialog_edit
import data.design_main


class CatMovie:
    id = None
    name = None
    orig_name = None
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
        if item is None:
            with open("data/placeholder.png", mode='rb') as f:
                image_binary = f.read()
                self.poster = image_binary
            return
        if len(item) == 12+13:
            st = 12
            self.id = item[st]
            self.name = item[st+1] if item[st+1] is not None else item[st+2]
            self.orig_name = item[st+2]
            self.year = int(item[st+3])
            self.country = item[st+4]
            self.genre = item[st+5]
            self.length = int(item[st+6])
            self.rating = item[st+7]
            self.director = item[st+8]
            self.script = item[st+9]
            self.actors = item[st+10]
            self.description = item[st+11]
            self.poster = item[st+12]
        else:
            self.id = item[0]
            self.name = item[1] if item[1] is not None else item[2]
            self.orig_name = item[2]
            self.year = int(item[3])
            self.country = item[4]
            self.genre = item[5]
            self.length = int(item[6])
            self.rating = item[7]
            self.director = item[8]
            self.script = item[9]
            self.actors = item[10]
            self.description = item[11]
            self.poster = item[12]

    def get_values_list(self):
        return [self.id, self.name, self.orig_name if self.orig_name is not None else self.name, self.year, self.country, self.genre, self.length, self.rating, self.director, self.script, self.actors, self.description, self.poster]

    def fill_widget(self, widget):
        if isinstance(widget, data.design_main.Ui_MainWindow):
            widget: data.design_main.Ui_MainWindow

            self.show_poster(widget.label_poster)

            widget.label_movie_name.setText(self.name)
            widget.label_orig_name.setText(self.orig_name)
            widget.label_year.setText(str(self.year))
            widget.label_country.setText(self.country)
            widget.label_genre.setText(self.genre.replace(",", ", "))
            widget.label_movie_length.setText(str(self.length))
            widget.label_rating.setText(self.rating)
            widget.label_director.setText(self.director)
            widget.label_script.setText(self.script)
            widget.label_actors.setText(self.actors)

            widget.plainTextEdit_description.setPlainText(self.description)

        if isinstance(widget, data.design_dialog_edit.Ui_Dialog):
            widget: data.design_dialog_edit.Ui_Dialog

            self.show_poster(widget.label_poster)

            widget.lineEdit_movie_name.setText(self.name)
            widget.lineEdit_orig_name.setText(self.orig_name)
            widget.lineEdit_year.setText(str(self.year))
            widget.lineEdit_country.setText(self.country)
            widget.lineEdit_genre.setText(self.genre.replace(",", ", "))
            widget.lineEdit_movie_length.setText(str(self.length))
            widget.lineEdit_rating.setText(self.rating)
            widget.lineEdit_director.setText(self.director)
            widget.lineEdit_script.setText(self.script)
            widget.lineEdit_actors.setText(self.actors)

            widget.textEdit_description.setPlainText(self.description)

    def show_poster(self, label: QLabel):
        if self.poster is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(self.poster)
            pixmap = pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
        else:
            pixmap = QPixmap(":/newPrefix/placeholder.png")
            pixmap = pixmap.scaled(label.width(), label.height())
            label.setPixmap(pixmap)

    def load_from_widget(self, widget: data.design_dialog_edit.Ui_Dialog):
        self.name = widget.lineEdit_movie_name.text()
        self.orig_name = widget.lineEdit_orig_name.text()
        self.year = int(widget.lineEdit_year.text())
        self.country = widget.lineEdit_country.text()
        self.genre = widget.lineEdit_genre.text()
        self.length = float(widget.lineEdit_movie_length.text())
        self.rating = widget.lineEdit_rating.text()
        self.director = widget.lineEdit_director.text()
        self.script = widget.lineEdit_script.text()
        self.actors = widget.lineEdit_actors.text()
        self.description = widget.textEdit_description.toPlainText()

    def __str__(self):
        return self.name + " (" + self.orig_name + ")"

    def set_data(self, movie):
        if movie is None: return
        self.name = movie.name if movie.name is not None else movie.original_name
        self.orig_name = movie.orig_name
        self.year = movie.year
        self.country = movie.country
        self.genre = movie.genre
        self.length = movie.length
        self.rating = movie.rating
        self.director = movie.director
        self.script = movie.script
        self.actors = movie.actors
        self.description = movie.description
        self.poster = movie.poster
        return self
