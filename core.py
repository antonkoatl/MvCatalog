import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSettings
from PyQt5.QtWidgets import QApplication

from dbhelper import *
from file import CatFile
from movie import CatMovie
from video_util import VideoHelper


class CoreWorker(QObject):
    signal_add_items_to_list = pyqtSignal(list)
    signal_fill_items_to_list = pyqtSignal(list)
    signal_update_db_result = pyqtSignal(str)
    signal_send_file_to_editdialog = pyqtSignal(CatFile)
    signal_send_frames_to_editdialog = pyqtSignal(list)
    signal_update_progress_bar = pyqtSignal(int)
    signal_send_open_db_result = pyqtSignal(int)
    signal_update_poster_label = pyqtSignal(bytes)

    settings = QSettings("data/settings.ini", QSettings.IniFormat)

    breaker_parse_video = False

    def __init__(self):
        QObject.__init__(self)
        self.db_helper = DBHelper()

    def __del__(self):
        self.wait()

    @pyqtSlot(str)
    def request_list_data(self, command):
        if command == 'start_list':
            db_data = self.db_helper.get_list_data(True)
            list_data = [[CatMovie(item), CatFile(item)] if item is not None else None for item in db_data]
            self.signal_fill_items_to_list.emit(list_data)
            return

        if command == 'add_list':
            db_data = self.db_helper.get_list_data()
            list_data = [[CatMovie(item), CatFile(item)] if item is not None else None for item in db_data]
            self.signal_add_items_to_list.emit(list_data)
            return

    @pyqtSlot(CatMovie, CatFile)
    def update_db(self, movie: CatMovie, file: CatFile):
        movie.id, error = self.db_helper.update_movie(movie)

        if error is not None:
            self.signal_update_db_result.emit(error)
            return

        if file.movie_id == -1:
            file.movie_id = movie.id

        error = self.db_helper.update_file(file)
        if error is not None:
            self.signal_update_db_result.emit(error)
            return

        self.request_list_data('start_list')
        self.signal_update_db_result.emit(None)

    @pyqtSlot(CatFile)
    def removefrom_db(self, file):
        self.db_helper.remove_file(file)

    @pyqtSlot(str)
    def parse_video_file(self, fname):
        self.breaker_parse_video = False
        video = VideoHelper(fname)
        self.signal_send_file_to_editdialog.emit(video.file)

        N = 20
        for i in range(N):
            QApplication.processEvents()
            if self.breaker_parse_video:
                self.breaker_parse_video = not self.breaker_parse_video
                return

            frame = video.get_frame(i, N)
            if frame is not None:
                video.frames.append(frame)
                self.signal_update_progress_bar.emit(i)

        self.signal_send_frames_to_editdialog.emit(video.frames)
        self.breaker_parse_video = True

    @pyqtSlot(str)
    def new_db(self, fname):
        self.db_helper.conn = None

        if Path(fname).is_file():
            os.remove(fname)

        if self.db_helper.create_db(fname):
            self.settings.setValue("last_db", fname)
            self.request_list_data('start_list')
        else:
            pass

    @pyqtSlot(str)
    def open_db(self, fname):
        if fname != "":
            self.db_helper.db_file = fname

        if not Path(self.db_helper.db_file).is_file():
            return False

        self.db_helper.conn = None

        if self.db_helper.create_connection():
            # self.db_helper.fill_test_data()
            self.settings.setValue("last_db", self.db_helper.db_file)
            self.signal_send_open_db_result.emit(1)
        else:
            self.signal_send_open_db_result.emit(0)

    @pyqtSlot(str)
    def load_poster(self, fname):
        if fname:
            with open(fname, mode='rb') as f:
                image_binary = f.read()

                self.signal_update_poster_label.emit(image_binary)
        else:
            self.signal_update_poster_label.emit(b'')

    @pyqtSlot(str)
    def set_breaker(self, name):
        if name == 'parse_video':
            self.breaker_parse_video = True
