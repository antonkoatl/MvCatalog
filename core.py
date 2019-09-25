from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from dbhelper import *

class CoreWorker(QObject):
    signal_add_items_to_list = pyqtSignal(list)
    signal_fill_items_to_list = pyqtSignal(list)

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
            list_data = self.db_helper.get_list_data(True)
            self.signal_fill_items_to_list.emit(list_data)
            return

        if command == 'add_list':
            list_data = self.db_helper.get_list_data()
            self.signal_add_items_to_list.emit(list_data)
            return

    @pyqtSlot(list)
    def update_db(self, data):
        movie = data[0]
        file = data[1]
        id = self.db_helper.add_movie(movie)
        if (file.movie_id == -1):
            file.movie_id = id
        self.db_helper.update_file(file)

        self.request_list_data('start_list')
