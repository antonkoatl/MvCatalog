from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
import data.design_dialog_edit
from file import CatFile
from movie import CatMovie


class EditDialog(QDialog, data.design_dialog_edit.Ui_Dialog):
    movie: CatMovie
    file: CatFile

    signal_db_updater = pyqtSignal(list)

    def __init__(self, parent=None):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click_save)

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
        self.file.length = int(self.lineEdit_16.text())
        self.file.audio = self.lineEdit_17.text()
        self.file.subtitles = self.lineEdit_18.text()

        self.signal_db_updater.emit([self.movie, self.file])

    def prepare(self, item=None):
        if item is None:
            self.movie = CatMovie()
            self.file = CatFile()
        else:
            self.movie = item[0]
            self.file = item[1]

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

            self.lineEdit_11.setText(self.file.name)
            self.lineEdit_12.setText(self.file.size)
            self.lineEdit_13.setText(self.file.resolution)
            self.lineEdit_14.setText(self.file.codec)
            self.lineEdit_15.setText(str(self.file.bitrate))
            self.lineEdit_16.setText(str(self.file.length))
            self.lineEdit_17.setText(self.file.audio)
            self.lineEdit_18.setText(self.file.subtitles)

            pixmap = QPixmap()
            pixmap.loadFromData(self.movie.poster)
            pixmap = pixmap.scaled(self.label_12.width(), self.label_12.height(), Qt.KeepAspectRatio)
            self.label_12.setPixmap(pixmap)

    @pyqtSlot(str)
    def update_db_result(self, error):
        if error != "":
            QMessageBox.warning(self, "Warning", error)
        else:
            self.accept()
