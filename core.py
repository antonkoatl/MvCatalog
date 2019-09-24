from PyQt5.QtCore import QThread, pyqtSignal
from dbhelper import *
import time

class CoreThread(QThread):
    sig1 = pyqtSignal(list)

    def __init__(self):
        QThread.__init__(self)
        self.db_helper = DBHelper()

    def __del__(self):
        self.wait()

    def run(self):
        self.db_helper.connect()
        self.db_helper.fill_test_data()
        list_data = self.db_helper.get_list()
        self.sig1.emit(list_data)


