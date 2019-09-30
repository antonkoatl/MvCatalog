from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QEvent
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
import data.design_dialog_edit
from file import CatFile
from movie import CatMovie


class EditDialog(QDialog, data.design_dialog_edit.Ui_Dialog):
    movie: CatMovie
    file: CatFile

    signal_db_updater = pyqtSignal(CatMovie, CatFile)
    signal_parse_video = pyqtSignal(str)

    def __init__(self, parent=None):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click_save)
        self.pushButton_2.clicked.connect(self.on_click_openfile)
        self.horizontalSlider.valueChanged.connect(self.slider_changed)


    @pyqtSlot()
    def on_click_save(self):
        self.movie.load_from_widget(self)
        self.file.load_from_widget(self)
        self.signal_db_updater.emit(self.movie, self.file)

    @pyqtSlot()
    def on_click_openfile(self):
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file', '.')
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


    def prepare(self, movie: CatMovie = None, file: CatFile = None):
        if movie is None:
            self.movie = CatMovie()
        else:
            self.movie = movie
            self.movie.fill_widget(self)

        if file is None:
            self.file = CatFile()
        else:
            self.file = file
            self.file.fill_widget(self)
