from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QFileDialog


class PosterLabel(QLabel):
    signal_load_poster = pyqtSignal(str)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        super(QLabel, self).mousePressEvent(ev)
        if (ev.button() == Qt.LeftButton):
            fname, _filter = QFileDialog.getOpenFileName(self, 'Open file', filter='Images (*.png .jpg)')
            if fname:
                self.signal_load_poster.emit(fname)

        if (ev.button() == Qt.RightButton):
            self.signal_load_poster.emit(None)
