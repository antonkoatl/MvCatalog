from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QCompleter

class ExtendedComboBox(QComboBox):
    signal_send_movie = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)
        self.movies = []
        self.skip_next_complete = False

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        #self.pFilterModel = QSortFilterProxyModel(self)
        #self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        #self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.model(), self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        #self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)
        self.activated[str].connect(self.on_activated)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    def on_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.signal_send_movie.emit(self.movies[index])

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

    def showPopup(self):
        super(ExtendedComboBox, self).showPopup()

    @pyqtSlot(list)
    def update_movies_list(self, result):
        self.movies = result

        # save text because it will be cleared
        text = self.lineEdit().text()
        self.clear()
        self.lineEdit().setText(text)

        self.addItems([i[1] for i in result])
        if self.skip_next_complete: self.complete = True
        else: self.completer.complete()
