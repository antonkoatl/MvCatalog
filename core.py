from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from dbhelper import *
import time

class CoreThread(QThread):
    sig1 = pyqtSignal(list)

    def __init__(self):
        QThread.__init__(self)
        self.db_helper = DBHelper()

    def __del__(self):
        self.wait()

    @pyqtSlot(str)
    def request_list_data(self, command):
        if command == 'start':
            self.db_helper.connect()
            self.db_helper.fill_test_data()
            return

        if command == 'fetch_list':
            list_data = self.db_helper.get_list()
            self.sig1.emit(list_data)
            return



