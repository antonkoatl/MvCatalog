from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QSlider


class MySlider(QSlider):

    def __init__(self, *__args):
        super(MySlider, self).__init__(*__args)
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def mouseMoveEvent(self, e: QMouseEvent, *args, **kwargs):
        if self.maximum() > 0:
            position = round(self.maximum() * e.x() / self.width())
            self.setValue(position)

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick):
            if event.button() == Qt.LeftButton:
                return True
        return super(QSlider, self).eventFilter(obj, event)
