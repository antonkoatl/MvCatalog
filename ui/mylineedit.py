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

    DEBUG = False

    def __init__(self, parent=None):
        super(ExtendedLineEdit, self).__init__(parent)
        self.movies = []

        self.completer_lw = QListWidget()
        self.model = self.completer_lw.model()

        self.completer = QCompleter(self.model, self)
        self.completer.setPopup(self.completer_lw)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.completer.setCompletionRole(Qt.UserRole) # Change role because default EditRole is paited to list somehow
        self.setCompleter(self.completer)

        self.textEdited.connect(self.text_edited)
        #self.completer.activated[QModelIndex].connect(self.on_completer_activated)
        #self.completer.activated[str].connect(self.on_completer_activated_str)
        self.completer_lw.itemClicked.connect(self.item_clicked)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.completer.complete()
        return super(ExtendedLineEdit, self).eventFilter(obj, event)

    def setText(self, text: str) -> None:
        if self.DEBUG: print('setText', text, self.sender())
        super(ExtendedLineEdit, self).setText(text)
        if not isinstance(self.sender(), QCompleter) and text:
            self.text_edited(text)

    @pyqtSlot(list)
    def update_movies_list(self, result):
        if self.DEBUG: print('update_movies_list', result[0], len(result) - 1)
        type = result.pop(0)

        if type == 'db':
            self.movies = [x + [type, ] for x in result]
            self.completer_lw.clear()
            self.completer.complete()
        else:
            for item in result:
                self.movies.append(item + [type,])

        for item in result:
            cwidget = MyWidget()
            cwidget.label_movie_name.setText(item[1] if item[1] else item[2])
            cwidget.label_original_name.setText(item[2])
            cwidget.label_source.setText(type)
            cwidget.label_year.setText(str(item[3]))

            completer_myQListWidgetItem = QListWidgetItem(self.completer_lw)
            completer_myQListWidgetItem.setSizeHint(cwidget.sizeHint())
            completer_myQListWidgetItem.setData(Qt.UserRole, item[1])
            self.completer_lw.addItem(completer_myQListWidgetItem)
            self.completer_lw.setItemWidget(completer_myQListWidgetItem, cwidget)

        if self.hasFocus() and not self.completer_lw.isVisible() and len(self.movies) > 0:
            self.completer.complete()

    @pyqtSlot(str)
    def text_edited(self, text):
        if self.DEBUG: print('text_edited', text, self.sender())
        if text and isinstance(self.sender(), ExtendedLineEdit):
            self.signal_search_movie.emit(text)

    @pyqtSlot(str)
    def on_completer_activated_str(self, name: str):
        if self.DEBUG: print('on_completer_activated_str', name)

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
        if self.DEBUG: print('reset')
        self.completer_lw.clear()
        self.clearFocus()
        #self.completer.activated[QModelIndex].connect(self.on_completer_activated)
