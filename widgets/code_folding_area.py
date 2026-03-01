from PySide6 import QtWidgets, QtCore, QtGui

class CodeFoldingArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(20, 0)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), QtGui.QColor(self.editor.theme_manager.get_color("fold", "#252526")))

        block = self.editor.firstVisibleBlock()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and self.editor.is_foldable(block):
                painter.setPen(QtGui.QColor(self.editor.theme_manager.get_color("lineNumbers", "#858585")))
                rect = QtCore.QRect(2, int(top) + 2, 16, 16)
                if self.editor.is_folded(block):
                    painter.drawText(rect, QtCore.Qt.AlignCenter, "+")
                else:
                    painter.drawText(rect, QtCore.Qt.AlignCenter, "-")
            block = block.next()
            top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()

    def mousePressEvent(self, event):
        block = self.editor.cursorForPosition(QtCore.QPoint(0, event.pos().y())).block()
        if block.isValid() and self.editor.is_foldable(block):
            self.editor.toggle_fold(block)