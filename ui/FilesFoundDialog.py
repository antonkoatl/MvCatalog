from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QApplication, QStyle

import data.design_dialog_found_files
from file import CatFile
from movie import CatMovie


class FilesFoundDialog(QDialog, data.design_dialog_found_files.Ui_Dialog):
    signal_parse_file = pyqtSignal(str)
    signal_send_breaker = pyqtSignal(str)
    signal_db_updater = pyqtSignal(CatMovie, CatFile)
    signal_send_breaker = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FilesFoundDialog, self).__init__(parent)
        self.setupUi(self)

        self.current_item = None
        self.file = None
        self.progressBar.setMaximum(20 - 1)

        self.pushButton_add.clicked.connect(self.add_files)

    def prepare(self):
        self.progressBar.setValue(0)
        self.listWidget.clear()

    def closeEvent(self, event):
        self.current_item = None
        self.file = None
        self.signal_send_breaker.emit('filesfound_dialog')

    @pyqtSlot(str)
    def add_file_to_list(self, data):
        print(data)
        myQListWidgetItem = QListWidgetItem(data.split('/')[-1])
        # myQListWidgetItem.setSizeHint(cwidget.sizeHint())
        myQListWidgetItem.setData(Qt.UserRole, data)
        myQListWidgetItem.setFlags(myQListWidgetItem.flags() | Qt.ItemIsUserCheckable)
        myQListWidgetItem.setCheckState(Qt.Checked)
        self.listWidget.addItem(myQListWidgetItem)

    @pyqtSlot()
    def add_files(self):
        for i in range(self.listWidget.count()):
            lw_item = self.listWidget.item(i)
            if not lw_item.checkState(): continue
            lw_item.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))
            lw_item.setFlags(lw_item.flags() & Qt.ItemIsSelectable)
            file_name = lw_item.data(Qt.UserRole)
            self.current_item = i
            self.signal_parse_file.emit(file_name)
            break

    @pyqtSlot(CatFile)
    def receive_parsed_file(self, file: CatFile):
        self.file = file

    @pyqtSlot(list)
    def receive_parsed_frames(self, frames):
        if self.file is not None:
            self.file.frames = frames
            self.listWidget.takeItem(self.current_item)

            movie = CatMovie()
            movie.name = self.file.name
            self.signal_db_updater.emit(movie, self.file)

            self.add_files()
