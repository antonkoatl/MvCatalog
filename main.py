import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QTreeWidgetItem

import data.design_main
from core import *
from edit_dialog import EditDialog
from ui.FilesFoundDialog import FilesFoundDialog
from file import CatFile
from movie import CatMovie


class MyWindow(QtWidgets.QMainWindow, data.design_main.Ui_MainWindow):
    signal_db_request = pyqtSignal(str)
    signal_db_updater = pyqtSignal(CatMovie, CatFile)
    signal_db_remover = pyqtSignal(CatFile)
    signal_db_new = pyqtSignal(str)
    signal_db_open = pyqtSignal(str)
    signal_scan_files = pyqtSignal(str)

    settings: QSettings = QSettings("data/settings.ini", QSettings.IniFormat)

    def __init__(self):
        super(MyWindow, self).__init__()

        #uic.loadUi('data/main.ui', self)
        self.setupUi(self)

        if not self.settings.value("geometry") == None:
            self.restoreGeometry(self.settings.value("geometry"))
        if not self.settings.value("windowState") == None:
            self.restoreState(self.settings.value("windowState"))

        self.list_data = []
        self.current_item_index = -1
        self.list_continues = False

        self.myThread = QThread(self)
        self.myThread.start()

        self.core_worker = CoreWorker()
        self.core_worker.db_helper.db_file = self.settings.value("last_db", "", str)
        self.core_worker.moveToThread(self.myThread)

        self.core_worker.signal_fill_items_to_list.connect(self.fill_records_list)
        self.core_worker.signal_add_items_to_list.connect(self.add_records_list)
        self.core_worker.signal_add_items_to_files_tree.connect(self.fill_files_tree)
        self.signal_db_updater.connect(self.core_worker.update_db)
        self.signal_db_remover.connect(self.core_worker.removefrom_db)
        self.signal_db_request.connect(self.core_worker.request_list_data)
        self.signal_db_new.connect(self.core_worker.new_db)
        self.signal_db_open.connect(self.core_worker.open_db)

        self.edit_dialog = EditDialog(self)
        self.edit_dialog.signal_db_updater.connect(self.core_worker.update_db)
        self.edit_dialog.signal_parse_video.connect(self.core_worker.parse_video_file)
        self.edit_dialog.label_poster.signal_load_poster.connect(self.core_worker.load_poster)
        self.edit_dialog.signal_send_breaker.connect(self.core_worker.set_breaker)
        self.edit_dialog.lineEdit_movie_name.signal_search_movie.connect(self.core_worker.search_movie_name)
        self.edit_dialog.lineEdit_movie_name.signal_send_movie.connect(self.edit_dialog.receive_movie)
        self.edit_dialog.lineEdit_movie_name.signal_request_movie_data.connect(self.core_worker.get_movie_data_from_kinopoisk)
        self.edit_dialog.lineEdit_movie_name.signal_set_loading.connect(self.edit_dialog.set_loading)
        self.core_worker.signal_update_db_result.connect(self.edit_dialog.update_db_result)
        self.core_worker.signal_send_parsed_file.connect(self.edit_dialog.receive_file)
        self.core_worker.signal_send_parsed_frames.connect(self.edit_dialog.receive_frames)
        self.core_worker.signal_update_frames_progress_bar.connect(self.edit_dialog.progressBar.setValue)
        self.core_worker.signal_send_open_db_result.connect(self.open_db_listener)
        self.core_worker.signal_update_poster_label.connect(self.edit_dialog.update_poster)
        self.core_worker.signal_movie_search_result.connect(self.edit_dialog.lineEdit_movie_name.update_movies_list)
        self.core_worker.signal_send_movie_to_editdialog.connect(self.edit_dialog.receive_movie)
        self.core_worker.signal_set_loading.connect(self.edit_dialog.set_loading)

        self.files_dialog = FilesFoundDialog(self)
        self.signal_scan_files.connect(self.core_worker.scan_dir)
        self.files_dialog.signal_parse_file.connect(self.core_worker.parse_video_file)
        self.files_dialog.signal_db_updater.connect(self.core_worker.update_db)
        self.files_dialog.signal_send_breaker.connect(self.core_worker.set_breaker)
        self.core_worker.signal_send_file_to_filesdialog.connect(self.files_dialog.add_file_to_list)
        self.core_worker.signal_show_filesdialog.connect(self.show_filesdialog)
        self.core_worker.signal_send_parsed_file.connect(self.files_dialog.receive_parsed_file)
        self.core_worker.signal_send_parsed_frames.connect(self.files_dialog.receive_parsed_frames)
        self.core_worker.signal_update_frames_progress_bar.connect(self.files_dialog.progressBar.setValue)

        self.listWidget_movies.itemClicked.connect(self.list_item_clicked)
        self.listWidget_movies.clear()

        self.actionAdd_Action.triggered.connect(self.add_item)
        self.actionAdd_dir.triggered.connect(self.action_add_folder)

        self.pushButton.clicked.connect(self.edit_item)
        self.pushButton_2.clicked.connect(self.delete_item)

        self.horizontalSlider.valueChanged.connect(self.slider_changed)

        self.scrollArea.hide()

        self.action_file_new.triggered.connect(self.new_db)
        self.action_file_open.triggered.connect(self.open_db)

        self.tabWidget.currentChanged.connect(self.tab_selected)
        self.treeWidget_files.itemClicked.connect(self.files_tree_item_clicked)

        self.show()
        self.signal_db_open.emit(None)


    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        QtWidgets.QMainWindow.closeEvent(self, event)


    @pyqtSlot(list)
    def fill_records_list(self, data):
        self.listWidget_movies.clear()

        self.list_data = data[:-1]
        self.list_continues = data[-1] != None

        movie: CatMovie
        file: CatFile
        for movie, file in data[:-1]:
            self.listWidget_movies.addItem(movie.name, )

        if (self.list_continues):
            self.listWidget.addItem("More...", )

        if self.current_item_index != -1:
            self.listWidget_movies.setCurrentRow(self.current_item_index)
            self.list_item_clicked(self.listWidget_movies.item(self.current_item_index))


    @pyqtSlot(list)
    def add_records_list(self, data):
        if self.listWidget_movies.count() > 0 and self.listWidget_movies.item(self.listWidget_movies.count() - 1).text() == "Loading...":
            self.listWidget_movies.takeItem(self.listWidget_movies.count() - 1)
            self.listWidget_movies.setCurrentRow(-1)

        self.list_data += data[:-1]
        self.list_continues = data[-1] != None

        for item in data[:-1]:
            if item == None: break
            self.listWidget_movies.addItem(item[0].name, )

        if (self.list_continues):
            self.listWidget_movies.addItem("More...", )

    @pyqtSlot(dict)
    def fill_files_tree(self, data):
        self.treeWidget_files.clear()

        for key, items in data.items():
            root = QTreeWidgetItem(self.treeWidget_files, [key,])

            for item in items:
                tree_item = QTreeWidgetItem([item[0].name,])
                tree_item.setData(0, Qt.UserRole, item)
                root.addChild(tree_item)


            root.setExpanded(True)
            root.setFlags(root.flags() & ~Qt.ItemIsSelectable)

    @pyqtSlot(int)
    def open_db_listener(self, int):
        if int == 0:
            self.open_db()

        if int == 1:
            self.signal_db_request.emit("start_list")

    @pyqtSlot(QListWidgetItem)
    def list_item_clicked(self, item: QListWidgetItem):
        if item is None:
            self.scrollArea.hide()
            return

        index = self.listWidget_movies.currentRow()

        if item.text() == "More...":
            item.setText("Loading...")
            self.signal_db_request.emit("add_list")
            return

        if item.text() == "Loading...":
            return

        self.scrollArea.show()

        self.current_item_index = index
        movie: CatMovie = self.list_data[index][0]
        file: CatFile = self.list_data[index][1]



        movie.fill_widget(self)
        file.fill_widget(self)

    @pyqtSlot(QTreeWidgetItem)
    def files_tree_item_clicked(self, item: QTreeWidgetItem):
        movie, file = item.data(0, Qt.UserRole)
        self.scrollArea.show()
        movie.fill_widget(self)
        file.fill_widget(self)


    @pyqtSlot()
    def add_item(self):
        self.edit_dialog.prepare()
        if self.edit_dialog.exec_():
            #self.signal_db_updater.emit([self.edit_dialog.movie, self.edit_dialog.file])
            pass

    @pyqtSlot()
    def action_add_folder(self):
        from os import listdir
        from os.path import isfile, join, normpath

        dir_ = QFileDialog.getExistingDirectory(None, caption = 'Select a folder:', options = QFileDialog.ShowDirsOnly)
        #video_files = [(f, normpath(join(dir_, f))) for f in listdir(dir_) if isfile(join(dir_, f)) and f.split('.')[-1] in ['avi', 'mkv', 'mp4']]

        #if len(video_files) == 0:
        #    return

        #self.files_dialog.prepare()
        self.signal_scan_files.emit(dir_)
        #if self.files_dialog.exec_():
        #    pass

    @pyqtSlot()
    def edit_item(self):
        if self.current_item_index == -1: return
        self.edit_dialog.prepare(self.list_data[self.current_item_index][0], self.list_data[self.current_item_index][1])
        if self.edit_dialog.exec_():
            self.signal_db_updater.emit(self.edit_dialog.movie, self.edit_dialog.file)

    @pyqtSlot()
    def delete_item(self):
        if self.current_item_index == -1: return
        self.signal_db_remover.emit(self.list_data.pop(self.current_item_index)[1])
        self.listWidget_movies.takeItem(self.current_item_index)
        self.listWidget_movies.setCurrentRow(-1)
        self.current_item_index = -1
        self.list_item_clicked(None)

    @pyqtSlot()
    def slider_changed(self):
        file = self.list_data[self.current_item_index][1]
        file.show_frame(self.label_frames, self.sender().value())

    @pyqtSlot()
    def new_db(self):
        fname, _filter = QFileDialog.getSaveFileName(self, 'Open file', filter='*.mcat')
        self.signal_db_new.emit(fname)

    @pyqtSlot()
    def open_db(self):
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file', filter='*.mcat')
        self.signal_db_open.emit(fname)

    @pyqtSlot()
    def show_filesdialog(self):
        self.files_dialog.prepare()
        if self.files_dialog.exec_():
            pass

    @pyqtSlot(int)
    def tab_selected(self, index):
        if index == 0:
            self.signal_db_request.emit("start_list")

        if index == 1:
            self.signal_db_request.emit("start_files_tree")


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
