from PyQt5.QtCore import QAbstractListModel, pyqtSignal, pyqtSlot, Qt, QModelIndex, QStringListModel, QEvent
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QLineEdit, QListWidget, QCompleter, QWidget, QListWidgetItem

import data.listitem_search


class MyWidget(QWidget, data.listitem_search.Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        self.setupUi(self)

class ExtendedLineEdit(QLineEdit):
    signal_send_movie = pyqtSignal(list)
    signal_search_movie = pyqtSignal(str)
    signal_request_movie_data = pyqtSignal(int)
    signal_set_loading = pyqtSignal(str, bool)

    DEBUG = True

    def __init__(self, parent=None):
        super(ExtendedLineEdit, self).__init__(parent)
        self.movies = []
        self.skip_next_complete = False
        self.skip_next_complete_not_db = False

        self.completer_lw = QListWidget()

        self.model = QStringListModel(self)

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.model, self)
        self.completer.setPopup(self.completer_lw)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        self.textEdited.connect(self.text_edited)
        #self.completer.activated[QModelIndex].connect(self.on_completer_activated)
        self.completer_lw.itemClicked.connect(self.item_clicked)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.completer.complete()
        return super(ExtendedLineEdit, self).eventFilter(obj, event)

    def setText(self, text: str) -> None:
        super(ExtendedLineEdit, self).setText(text)
        if not isinstance(self.sender(), QCompleter) and text:
            self.skip_next_complete = True
            self.text_edited(text)

    @pyqtSlot(list)
    def update_movies_list(self, result):
        if self.DEBUG: print('update_movies_list', result)
        type = result.pop(0)


        if type == 'db':
            self.movies = [x + [type, ] for x in result]
            self.completer_lw.clear()
            self.model.setStringList([item[1] for item in result])
        else:
            for item in result:
                self.movies.append(item + [type,])
                if self.model.insertRow(self.model.rowCount()):
                    index = self.model.index(self.model.rowCount() - 1, 0)
                    self.model.setData(index, item[1])

        for item in result:
            cwidget = MyWidget()
            cwidget.label_movie_name.setText(item[1] if item[1] else item[2])
            cwidget.label_original_name.setText(item[2])
            cwidget.label_source.setText(type)
            cwidget.label_year.setText(str(item[3]))

            completer_myQListWidgetItem = QListWidgetItem(self.completer_lw)
            completer_myQListWidgetItem.setSizeHint(cwidget.sizeHint())
            self.completer_lw.addItem(completer_myQListWidgetItem)
            self.completer_lw.setItemWidget(completer_myQListWidgetItem, cwidget)

        if self.skip_next_complete:
            if type == 'db':
                self.skip_next_complete_not_db = True
            self.skip_next_complete = False
        else:
            if type == 'db':
                self.completer.complete()
            else:
                if self.skip_next_complete_not_db:
                    self.skip_next_complete_not_db = False
                else:
                    self.completer.complete()

    @pyqtSlot(str)
    def text_edited(self, text):
        if self.DEBUG: print('text_edited', text, self.sender())
        if text and isinstance(self.sender(), ExtendedLineEdit):
            self.signal_search_movie.emit(text)

    @pyqtSlot(QModelIndex)
    def on_completer_activated(self, index: QModelIndex):
        if self.DEBUG: print('on_completer_activated', index.row())
        item = self.movies[index.row()]

        if len(item) > 13:
            self.signal_send_movie.emit(item[:13])
            self.signal_request_movie_data.emit(item[13])
        else:
            self.signal_send_movie.emit(item)

    @pyqtSlot(QListWidgetItem)
    def item_clicked(self, item: QListWidgetItem):
        if self.DEBUG: print('item_clicked', item, [i[1] for i in self.movies])
        index = self.completer_lw.indexFromItem(item)
        item = self.movies[index.row()]
        type = item[-1]

        if type == 'db':
            self.signal_send_movie.emit(item)
        else:
            self.signal_set_loading.emit('movie', True)

            if len(item) > 13:
                self.signal_send_movie.emit(item[:13])
                self.signal_request_movie_data.emit(item[13])
            else:
                self.signal_send_movie.emit(item)

    def reset(self):
        self.completer_lw.clear()
        #self.completer.activated[QModelIndex].connect(self.on_completer_activated)
