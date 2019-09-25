import sys, time
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QSettings, Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPixmap
from core import *
import data.design_main
from edit_dialog import EditDialog


class MyWindow(QtWidgets.QMainWindow, data.design_main.Ui_MainWindow):
    sig1 = pyqtSignal(str)
    signal_db_updater = pyqtSignal(list)
    list_data = []

    def __init__(self):
        super(MyWindow, self).__init__()
        self.list_continues = False
        self.settings = QSettings("MyCompany", "MyApp")
        #uic.loadUi('data/main.ui', self)
        self.setupUi(self)

        if not self.settings.value("geometry") == None:
            self.restoreGeometry(self.settings.value("geometry"))
        if not self.settings.value("windowState") == None:
            self.restoreState(self.settings.value("windowState"))

        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(""))

        for i in range(self.tableWidget_2.rowCount()):
            self.tableWidget_2.setItem(i, 0, QTableWidgetItem(""))

        self.listWidget.itemClicked.connect(self.list_item_clicked)
        self.listWidget.clear()

        self.show()
        self.myThread = QThread(self)
        self.myThread.start()

        self.core_worker = CoreWorker()
        self.core_worker.moveToThread(self.myThread)

        self.core_worker.signal_fill_items_to_list.connect(self.fill_records_list)
        self.core_worker.signal_add_items_to_list.connect(self.add_records_list)
        self.signal_db_updater.connect(self.core_worker.update_db)
        self.sig1.connect(self.core_worker.request_list_data)
        self.sig1.emit("start")
        self.sig1.emit("start_list")

        self.edit_dialog = EditDialog(self)

        self.actionAdd_Action.triggered.connect(self.add_item)


    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        QtWidgets.QMainWindow.closeEvent(self, event)

    @pyqtSlot(list)
    def fill_records_list(self, data):
        self.listWidget.clear()

        self.list_data = data[:-1]
        self.list_continues = data[-1] != None

        for item in data[:-1]:
            if item == None: break
            self.listWidget.addItem(item[12])

        if (self.list_continues):
            self.listWidget.addItem("More...")

    @pyqtSlot(list)
    def add_records_list(self, data):
        if self.listWidget.count() > 0 and self.listWidget.item(self.listWidget.count() - 1).text() == "Loading...":
            self.listWidget.takeItem(self.listWidget.count() - 1)
            self.listWidget.setCurrentRow(-1)

        self.list_data += data[:-1]
        self.list_continues = data[-1] != None

        for item in data[:-1]:
            if item == None: break
            self.listWidget.addItem(item[12])

        if (self.list_continues):
            self.listWidget.addItem("More...")

    def list_item_clicked(self, item):
        index = self.listWidget.currentRow()

        if item.text() == "More...":
            item.setText("Loading...")
            self.sig1.emit("add_list")
            return

        if item.text() == "Loading...":
            return

        pixmap = QPixmap()
        pixmap.loadFromData(self.list_data[index][22])
        pixmap = pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

        for i in range(self.tableWidget_2.rowCount()):
            self.tableWidget_2.item(i, 0).setText(str(self.list_data[index][i+2]))

        for i in range(self.tableWidget.rowCount()):
            j = i + self.tableWidget_2.rowCount()
            self.tableWidget.item(i, 0).setText(str(self.list_data[index][j+3]))

    def add_item(self):
        self.edit_dialog.prepare()
        if self.edit_dialog.exec_():
            self.signal_db_updater.emit([self.edit_dialog.movie, self.edit_dialog.file])


if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
