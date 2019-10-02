from PyQt5.QtCore import QAbstractListModel, pyqtSignal, pyqtSlot, Qt, QModelIndex, QStringListModel, QEvent
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QLineEdit, QListWidget, QCompleter, QWidget, QListWidgetItem

import data.listitem_search


class MyWidget(QWidget, data.listitem_search.Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        self.setupUi(self)

class ExtendedLineEdit(QLineEdit):
    signal_send_movie = pyqtSignal(tuple)
    signal_search_movie = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExtendedLineEdit, self).__init__(parent)
        self.movies = []
        self.skip_next_complete = False

        self.completer_lw = QListWidget()

        self.model = QStringListModel(self)

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.model, self)
        self.completer.setPopup(self.completer_lw)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        self.textEdited.connect(self.text_edited)
        self.completer.activated[QModelIndex].connect(self.on_completer_activated)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.completer.complete()
        return super(ExtendedLineEdit, self).eventFilter(obj, event)

    def setText(self, text: str) -> None:
        super(ExtendedLineEdit, self).setText(text)
        if not isinstance(self.sender(), QCompleter):
            self.skip_next_complete = True
            self.text_edited(text)

    @pyqtSlot(list)
    def update_movies_list(self, result):
        self.movies = result

        self.completer_lw.clear()
        self.model.setStringList([i[1] for i in result])

        for item in result:
            cwidget = MyWidget()
            cwidget.label.setText(item[1])
            cwidget.label_2.setText(item[2])

            completer_myQListWidgetItem = QListWidgetItem(self.completer_lw)
            self.completer_lw.addItem(completer_myQListWidgetItem)
            self.completer_lw.setItemWidget(completer_myQListWidgetItem, cwidget)

        if self.skip_next_complete:
            self.skip_next_complete = False
        else:
            self.completer.complete()

    @pyqtSlot(str)
    def text_edited(self, text):
        if text:
            self.signal_search_movie.emit(text)

    @pyqtSlot(QModelIndex)
    def on_completer_activated(self, index: QModelIndex):
        self.signal_send_movie.emit(self.movies[index.row()])

    @pyqtSlot(QListWidgetItem)
    def item_clicked(self, item: QListWidgetItem):
        index = self.completer_lw.indexFromItem(item)
        self.signal_send_movie.emit(self.movies[index.row()])

    def reset(self):
        self.completer_lw.clear()
        self.completer.activated[QModelIndex].connect(self.on_completer_activated)
