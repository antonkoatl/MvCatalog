from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from dbhelper import *
from file import CatFile
from movie import CatMovie


class CoreWorker(QObject):
    signal_add_items_to_list = pyqtSignal(list)
    signal_fill_items_to_list = pyqtSignal(list)
    signal_update_result = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        self.db_helper = DBHelper()

    def __del__(self):
        self.wait()

    @pyqtSlot(str)
    def request_list_data(self, command):
        if command == 'start':
            self.db_helper.connect()
            self.db_helper.fill_test_data()
            return

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

    @pyqtSlot(list)
    def update_db(self, data):
        movie = data[0]
        file = data[1]
        movie.id, error = self.db_helper.update_movie(movie)

        if error is not None:
            self.signal_update_result.emit(error)
            return

        if file.movie_id == -1:
            file.movie_id = movie.id

        error = self.db_helper.update_file(file)
        if error is not None:
            self.signal_update_result.emit(error)
            return

        self.request_list_data('start_list')
        self.signal_update_result.emit(None)

    @pyqtSlot(CatFile)
    def removefrom_db(self, file):
        self.db_helper.remove_file(file)
