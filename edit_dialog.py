from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog

import data.design_dialog_edit
from file import CatFile
from movie import CatMovie


class EditDialog(QDialog, data.design_dialog_edit.Ui_Dialog):
    movie: CatMovie
    file: CatFile

    signal_db_updater = pyqtSignal(CatMovie, CatFile)
    signal_parse_video = pyqtSignal(str)
    signal_send_breaker = pyqtSignal(str)

    def __init__(self, parent=None):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_save.clicked.connect(self.on_click_save)
        self.pushButton_open.clicked.connect(self.on_click_openfile)
        self.horizontalSlider.valueChanged.connect(self.slider_changed)

        self.loading = False
        self.loader_movie: QMovie = QMovie('data/loader.gif')
        self.label_loading.setMovie(self.loader_movie)

    def closeEvent(self, event):
        self.signal_send_breaker.emit('parse_video')


    @pyqtSlot()
    def on_click_save(self):
        self.movie.load_from_widget(self)
        self.file.load_from_widget(self)
        self.signal_db_updater.emit(self.movie, self.file)

    @pyqtSlot()
    def on_click_openfile(self):
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file', filter='Video (*.mkv .avi .mp4 .webm)')
        if fname:
            self.set_loading(True)
            self.progressBar.setMaximum(20-1)
            self.signal_parse_video.emit(fname)

    @pyqtSlot()
    def slider_changed(self):
        self.file.show_frame(self.label_frames, self.sender().value())

    @pyqtSlot(str)
    def update_db_result(self, error):
        if error != "":
            QMessageBox.warning(self, "Warning", error)
        else:
            self.accept()

    @pyqtSlot(CatFile)
    def receive_file(self, file: CatFile):
        self.file = file
        self.file.fill_widget(self)

    @pyqtSlot(list)
    def receive_frames(self, frames):
        self.file.frames = frames

        self.horizontalSlider.setMaximum(len(self.file.frames) - 1)
        self.file.show_frame(self.label_frames, 0)
        self.set_loading(False)

    @pyqtSlot(bytes)
    def update_poster(self, image):
        if not image: image = None
        self.movie.poster = image
        self.movie.show_poster(self.label_poster)

    @pyqtSlot(tuple)
    def receive_movie(self, data):
        self.movie = CatMovie(data)
        self.movie.fill_widget(self)


    def prepare(self, movie: CatMovie = None, file: CatFile = None):
        if movie is None:
            self.movie = CatMovie()
            self.movie.fill_widget(self)
        else:
            self.movie = movie
            self.comboBox_movie_name.skip_next_complete = True
            self.movie.fill_widget(self)

        if file is None:
            self.file = CatFile()
            self.file.fill_widget(self)
        else:
            self.file = file
            self.file.fill_widget(self)

        self.set_loading(False)
        self.progressBar.setValue(0)

    def set_loading(self, loading):
        self.loading = loading
        if loading:
            self.label_loading.setMovie(self.loader_movie)
            self.loader_movie.start()
            self.pushButton_save.setEnabled(False)
        else:
            self.label_loading.clear()
            self.loader_movie.stop()
            self.pushButton_save.setEnabled(True)
