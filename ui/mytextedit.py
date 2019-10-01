from PyQt5.QtWidgets import QPlainTextEdit


class GrowingTextEdit(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().setDocumentMargin(0)

        #self.document().contentsChanged.connect(self.sizeChange)
        self.document().documentLayout().documentSizeChanged.connect(self.wrapHeightToContents)

        self.height_min = 0
        self.height_max = 65000

    def wrapHeightToContents(self):
        doc_height = self.document().size().height()
        if self.height_min <= doc_height <= self.height_max:

            doc = self.document()
            layout = doc.documentLayout()
            h = 0
            b = doc.begin()
            while b != doc.end():
                h += layout.blockBoundingRect(b).height()
                b = b.next()

            # +1 to prevent scroll
            self.setFixedHeight(h + doc.documentMargin() + 1)
