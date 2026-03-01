from PySide6 import QtWidgets, QtCore, QtGui
from widgets.line_number_area import LineNumberArea
from widgets.code_folding_area import CodeFoldingArea
import os

class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, theme_manager, extension_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.extension_manager = extension_manager

        # Font
        self.setFont(QtGui.QFont("Consolas", 12))
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setTabStopDistance(QtGui.QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)

        # Folding
        self.folded_blocks = set()

        # Side widgets
        self.line_number_area = LineNumberArea(self)
        self.folding_area = CodeFoldingArea(self)

        # Signals
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Autosave timer
        self.auto_save_timer = QtCore.QTimer()
        self.auto_save_timer.setInterval(30000)
        self.auto_save_timer.timeout.connect(self.auto_save)

        self.is_modified = False
        self.document().modificationChanged.connect(self.set_modified)
        self.file_path = None
        self.highlighter = None

        # Apply initial theme
        self.apply_theme()

    def apply_theme(self):
        # Обновляем цвета в соответствии с текущей темой
        bg = self.theme_manager.get_color("background", "#1e1e1e")
        fg = self.theme_manager.get_color("foreground", "#d4d4d4")
        sel = self.theme_manager.get_color("selection", "#264f78")
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {bg};
                color: {fg};
                border: none;
                selection-background-color: {sel};
            }}
        """)
        # Пересоздаём highlighter с новыми цветами
        if self.file_path:
            self.set_language_from_file(self.file_path)
        else:
            self.highlighter = None

    def set_modified(self, modified):
        self.is_modified = modified

    def auto_save(self):
        if self.is_modified and self.file_path:
            self.save_file(self.file_path)

    def save_file(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.toPlainText())
            self.document().setModified(False)
            self.is_modified = False
            return True
        except Exception:
            return False

    def load_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.setPlainText(f.read())
            self.file_path = file_path
            self.document().setModified(False)
            self.is_modified = False
            self.set_language_from_file(file_path)
            return True
        except Exception:
            return False

    def set_language_from_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        print(f"Setting language for file {file_path}, extension: {ext}")  # отладка
        highlighter_class = self.extension_manager.get_highlighter_for_file(file_path, self.theme_manager)
        if highlighter_class:
            print(f"Found highlighter for {ext}, applying...")  # отладка
            self.highlighter = highlighter_class
            self.highlighter.setDocument(self.document())
        else:
            print(f"No highlighter found for {ext}")  # отладка
            self.highlighter = None

    def is_foldable(self, block):
        text = block.text().strip()
        # Простая эвристика для Python и C-подобных
        if text.endswith(':') and not text.startswith(('"""', "'''")):
            return True
        if text.endswith('{'):
            return True
        if text.startswith(('#if', '#ifdef', '#ifndef')):
            return True
        return False

    def is_folded(self, block):
        return block.blockNumber() in self.folded_blocks

    def toggle_fold(self, block):
        block_number = block.blockNumber()
        if block_number in self.folded_blocks:
            self.folded_blocks.remove(block_number)
            self.show_block(block.next())
        else:
            self.folded_blocks.add(block_number)
            self.hide_block(block.next())
        self.folding_area.update()
        self.line_number_area.update()

    def hide_block(self, block):
        if not block.isValid():
            return
        original_text = block.text()
        indent_level = len(original_text) - len(original_text.lstrip())
        while block.isValid():
            next_block = block.next()
            if not next_block.isValid():
                break
            next_text = next_block.text()
            next_indent = len(next_text) - len(next_text.lstrip())
            if next_indent <= indent_level:
                break
            next_block.setVisible(False)
            block = next_block

    def show_block(self, block):
        if not block.isValid():
            return
        parent_block = block.previous()
        while parent_block.isValid():
            if parent_block.blockNumber() in self.folded_blocks:
                return
            parent_block = parent_block.previous()
        while block.isValid() and not block.isVisible():
            block.setVisible(True)
            block = block.next()

    def keyPressEvent(self, event):
        # Auto-indent and bracket closing
        if event.key() == QtCore.Qt.Key.Key_Tab:
            cursor = self.textCursor()
            if cursor.hasSelection():
                self.indent_selection()
            else:
                super().keyPressEvent(event)
        elif event.key() == QtCore.Qt.Key.Key_Backtab:
            self.unindent_selection()
        elif event.key() == QtCore.Qt.Key.Key_Return:
            super().keyPressEvent(event)
            self.auto_indent()
        elif event.key() == QtCore.Qt.Key.Key_BraceLeft:
            super().keyPressEvent(event)
            self.textCursor().insertText('}')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        elif event.key() == QtCore.Qt.Key.Key_ParenLeft:
            super().keyPressEvent(event)
            self.textCursor().insertText(')')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        elif event.key() == QtCore.Qt.Key.Key_BracketLeft:
            super().keyPressEvent(event)
            self.textCursor().insertText(']')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        elif event.key() == QtCore.Qt.Key.Key_QuoteDbl:
            super().keyPressEvent(event)
            self.textCursor().insertText('"')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        else:
            super().keyPressEvent(event)

    def indent_selection(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        while cursor.position() <= end:
            cursor.insertText('    ')
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextBlock)
            if cursor.atEnd():
                break
        cursor.endEditBlock()

    def unindent_selection(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        while cursor.position() <= end:
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextCharacter,
                                QtGui.QTextCursor.MoveMode.KeepAnchor, 4)
            if cursor.selectedText() == '    ':
                cursor.removeSelectedText()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextBlock)
            if cursor.atEnd():
                break
        cursor.endEditBlock()

    def auto_indent(self):
        cursor = self.textCursor()
        block = cursor.block()
        text = block.text()
        indent = len(text) - len(text.lstrip())
        if text.rstrip().endswith(':'):
            indent += 4
        if indent > 0:
            cursor.insertText(' ' * indent)

    def line_number_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, new_block_count):
        self.setViewportMargins(self.line_number_width() + 20, 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
            self.folding_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
            self.folding_area.update(0, rect.y(), self.folding_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        line_width = self.line_number_width()
        self.line_number_area.setGeometry(QtCore.QRect(cr.left(), cr.top(), line_width, cr.height()))
        self.folding_area.setGeometry(QtCore.QRect(cr.left() + line_width, cr.top(), 20, cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QtGui.QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QtGui.QColor(self.theme_manager.get_color("background", "#1e1e1e")))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtGui.QColor(self.theme_manager.get_color("lineNumbers", "#858585")))
                painter.setFont(self.font())
                painter.drawText(0, int(top), self.line_number_area.width() - 2,
                                 self.fontMetrics().height(), QtCore.Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = QtGui.QColor(self.theme_manager.get_color("lineHighlight", "#2a2a2a"))
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)