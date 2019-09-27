from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
import data.design_dialog_edit
from file import CatFile
from movie import CatMovie
from video_util import VideoHelper


class EditDialog(QDialog, data.design_dialog_edit.Ui_Dialog):
    movie: CatMovie
    file: CatFile

    signal_db_updater = pyqtSignal(list)

    def __init__(self, parent=None):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click_save)
        self.pushButton_2.clicked.connect(self.on_click_openfile)
        self.horizontalSlider.valueChanged.connect(self.slider_changed)

        with open("data/placeholder.png", mode='rb') as f:
            image_binary = f.read()
            placeholder_poster = image_binary
            pixmap = QPixmap()
            pixmap.loadFromData(placeholder_poster)
            pixmap = pixmap.scaled(self.label_12.width(), self.label_12.height(), Qt.KeepAspectRatio)
            self.label_12.setPixmap(pixmap)


    def on_click_save(self):
        self.movie.name = self.lineEdit.text()
        self.movie.orig_name = self.lineEdit_2.text()
        self.movie.year = int(self.lineEdit_3.text())
        self.movie.country = self.lineEdit_4.text()
        self.movie.genre = self.lineEdit_5.text()
        self.movie.length = int(self.lineEdit_6.text())
        self.movie.rating = self.lineEdit_7.text()
        self.movie.director = self.lineEdit_8.text()
        self.movie.script = self.lineEdit_9.text()
        self.movie.actors = self.lineEdit_10.text()
        self.movie.description = self.textEdit.toPlainText()

        self.file.name = self.lineEdit_11.text()
        self.file.size = self.lineEdit_12.text()
        self.file.resolution = self.lineEdit_13.text()
        self.file.codec = self.lineEdit_14.text()
        self.file.bitrate = int(self.lineEdit_15.text())
        self.file.length = float(self.lineEdit_16.text())
        self.file.audio = self.lineEdit_17.text()
        self.file.subtitles = self.lineEdit_18.text()

        self.signal_db_updater.emit([self.movie, self.file])

    def on_click_openfile(self):
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file', '.')

        video = VideoHelper(fname)
        self.file = video.file
        self.prepare_file()

        video.get_frames()
        self.file.frames = video.frames

        self.horizontalSlider.setMaximum(len(self.file.frames) - 1)
        self.file.show_frame(self.label_23, 0)


    def slider_changed(self):
        self.file.show_frame(self.label_23, self.horizontalSlider.value())

    def prepare(self, item=None):
        if item is None:
            self.movie = CatMovie()
            self.file = CatFile()
        else:
            self.movie = item[0]
            self.file = item[1]

            self.prepare_movie()
            self.prepare_file()

            pixmap = QPixmap()
            pixmap.loadFromData(self.movie.poster)
            pixmap = pixmap.scaled(self.label_12.width(), self.label_12.height(), Qt.KeepAspectRatio)
            self.label_12.setPixmap(pixmap)

    def prepare_movie(self):
        self.lineEdit.setText(self.movie.name)
        self.lineEdit_2.setText(self.movie.orig_name)
        self.lineEdit_3.setText(str(self.movie.year))
        self.lineEdit_4.setText(self.movie.country)
        self.lineEdit_5.setText(self.movie.genre)
        self.lineEdit_6.setText(str(self.movie.length))
        self.lineEdit_7.setText(self.movie.rating)
        self.lineEdit_8.setText(self.movie.director)
        self.lineEdit_9.setText(self.movie.script)
        self.lineEdit_10.setText(self.movie.actors)
        self.textEdit.setText(self.movie.description)

    def prepare_file(self):
        self.lineEdit_11.setText(self.file.name)
        self.lineEdit_12.setText(self.file.size)
        self.lineEdit_13.setText(self.file.resolution)
        self.lineEdit_14.setText(self.file.codec)
        self.lineEdit_15.setText(str(self.file.bitrate))
        self.lineEdit_16.setText(str(self.file.length))
        self.lineEdit_17.setText(self.file.audio)
        self.lineEdit_18.setText(self.file.subtitles)

    @pyqtSlot(str)
    def update_db_result(self, error):
        if error != "":
            QMessageBox.warning(self, "Warning", error)
        else:
            self.accept()
