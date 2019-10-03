import array
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import data.design_main, data.design_dialog_edit
import pickle

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
    frames = []


    def __init__(self, item=None):
        if item is None: return
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
        self.frames = self.get_frames_from_blob(item[10])

    def get_values_list(self):
        return [self.id, self.movie_id, self.name, self.size, self.resolution, self.codec, self.bitrate, self.length, self.audio, self.subtitles, self.get_frames_as_blob()]

    def fill_widget(self, widget):
        if isinstance(widget, data.design_main.Ui_MainWindow):
            widget: data.design_main.Ui_MainWindow

            widget.plainTextEdit_file_name.setPlainText(self.name)
            widget.label_size.setText(self.size)
            widget.label_resolution.setText(self.resolution)
            widget.label_codec.setText(self.codec)
            widget.label_bitrate.setText(str(self.bitrate))
            widget.label_file_length.setText(str(self.length))
            widget.label_audio.setText(self.audio)
            widget.label_subs.setText(self.subtitles)

            widget.horizontalSlider.setMaximum(max(len(self.frames) - 1, 0))
            widget.horizontalSlider.setValue(-1)
            widget.horizontalSlider.setValue(widget.horizontalSlider.maximum() / 2)

        if isinstance(widget, data.design_dialog_edit.Ui_Dialog):
            widget: data.design_dialog_edit.Ui_Dialog

            widget.lineEdit_file_name.setText(self.name)
            widget.lineEdit_size.setText(self.size)
            widget.lineEdit_resolution.setText(self.resolution)
            widget.lineEdit_codec.setText(self.codec)
            widget.lineEdit_bitrate.setText(str(self.bitrate))
            widget.lineEdit_file_length.setText(str(self.length))
            widget.lineEdit_audio.setText(self.audio)
            widget.lineEdit_subs.setText(self.subtitles)

            widget.horizontalSlider.setMaximum(max(len(self.frames) - 1, 0))
            widget.horizontalSlider.setValue(-1)
            widget.horizontalSlider.setValue(widget.horizontalSlider.maximum() / 2)

    def load_from_widget(self, widget: data.design_dialog_edit.Ui_Dialog):
        self.name = widget.lineEdit_file_name.text()
        self.size = widget.lineEdit_size.text()
        self.resolution = widget.lineEdit_resolution.text()
        self.codec = widget.lineEdit_codec.text()
        self.bitrate = int(widget.lineEdit_bitrate.text())
        self.length = float(widget.lineEdit_file_length.text())
        self.audio = widget.lineEdit_audio.text()
        self.subtitles = widget.lineEdit_subs.text()

    def show_frame(self, label: QLabel, index):
        if index >= len(self.frames) or index == -1:
            pixmap = QPixmap(":/newPrefix/placeholder.png")
            pixmap = pixmap.scaled(label.width(), label.height())
            label.setPixmap(pixmap)
        else:
            pixmap = QPixmap()
            pixmap.loadFromData(self.frames[index])
            pixmap = pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio)
            label.setPixmap(pixmap)

    def get_frames_as_blob(self):
        return pickle.dumps(self.frames)

    def get_frames_from_blob(self, data):
        return [] if data is None else pickle.loads(data)

    def set_data(self, file):
        if file is None: return
        if self.movie_id == -1: self.movie_id = file.movie_id
        self.name = file.name
        self.size = file.size
        self.resolution = file.resolution
        self.codec = file.codec
        self.bitrate = file.bitrate
        self.length = file.length
        self.audio = file.audio
        self.subtitles = file.subtitles
        self.frames = file.frames
