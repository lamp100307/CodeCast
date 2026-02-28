import sys
import os
from PySide6 import QtWidgets, QtCore, QtGui

# ------------------------------- Base highlighter -------------------------------

class BaseHighlighter(QtGui.QSyntaxHighlighter):
    """Base class for syntax highlighting"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

# ------------------------------- Python highlighter -------------------------------

class PythonHighlighter(BaseHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Keywords
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor("#569CD6"))
        keyword_format.setFontWeight(QtGui.QFont.Weight.Bold)

        keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'with', 'yield',
            'None', 'True', 'False', 'as', 'async', 'await'
        ]

        for word in keywords:
            pattern = QtCore.QRegularExpression(r'\b' + word + r'\b')
            self.rules.append((pattern, keyword_format))

        # Strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor("#CE9178"))
        self.rules.append((QtCore.QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.rules.append((QtCore.QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # Comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor("#6A9955"))
        comment_format.setFontItalic(True)
        self.rules.append((QtCore.QRegularExpression(r'#[^\n]*'), comment_format))

        # Functions
        function_format = QtGui.QTextCharFormat()
        function_format.setForeground(QtGui.QColor("#DCDCAA"))
        self.rules.append((QtCore.QRegularExpression(r'\b[A-Za-z0-9_]+(?=\()'), function_format))

        # Decorators
        decorator_format = QtGui.QTextCharFormat()
        decorator_format.setForeground(QtGui.QColor("#D7BA7D"))
        self.rules.append((QtCore.QRegularExpression(r'^\s*@[A-Za-z_][A-Za-z0-9_]*'), decorator_format))

        # Numbers
        number_format = QtGui.QTextCharFormat()
        number_format.setForeground(QtGui.QColor("#B5CEA8"))
        self.rules.append((QtCore.QRegularExpression(r'\b[0-9]+\b'), number_format))

# ------------------------------- C/C++ highlighter -------------------------------

class CHighlighter(BaseHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Keywords
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor("#569CD6"))
        keyword_format.setFontWeight(QtGui.QFont.Weight.Bold)

        keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            'class', 'private', 'protected', 'public', 'namespace', 'using', 'this',
            'new', 'delete', 'throw', 'try', 'catch', 'virtual', 'override', 'final',
            'friend', 'operator', 'template', 'typename', 'explicit', 'static_cast',
            'dynamic_cast', 'const_cast', 'reinterpret_cast', 'bool', 'true', 'false'
        ]

        for word in keywords:
            pattern = QtCore.QRegularExpression(r'\b' + word + r'\b')
            self.rules.append((pattern, keyword_format))

        # Strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor("#CE9178"))
        self.rules.append((QtCore.QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.rules.append((QtCore.QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # Comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor("#6A9955"))
        comment_format.setFontItalic(True)
        self.rules.append((QtCore.QRegularExpression(r'//[^\n]*'), comment_format))
        self.rules.append((QtCore.QRegularExpression(r'/\*.*?\*/'), comment_format))

        # Preprocessor
        preprocessor_format = QtGui.QTextCharFormat()
        preprocessor_format.setForeground(QtGui.QColor("#D7BA7D"))
        self.rules.append((QtCore.QRegularExpression(r'^\s*#\s*[a-zA-Z]+'), preprocessor_format))

        # Numbers
        number_format = QtGui.QTextCharFormat()
        number_format.setForeground(QtGui.QColor("#B5CEA8"))
        self.rules.append((QtCore.QRegularExpression(r'\b[0-9]+\b'), number_format))
        self.rules.append((QtCore.QRegularExpression(r'\b0x[0-9a-fA-F]+\b'), number_format))

# ------------------------------- C# highlighter -------------------------------

class CSharpHighlighter(BaseHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor("#569CD6"))
        keyword_format.setFontWeight(QtGui.QFont.Weight.Bold)

        keywords = [
            'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch',
            'char', 'checked', 'class', 'const', 'continue', 'decimal', 'default',
            'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit',
            'extern', 'false', 'finally', 'fixed', 'float', 'for', 'foreach',
            'goto', 'if', 'implicit', 'in', 'int', 'interface', 'internal', 'is',
            'lock', 'long', 'namespace', 'new', 'null', 'object', 'operator',
            'out', 'override', 'params', 'private', 'protected', 'public',
            'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof',
            'stackalloc', 'static', 'string', 'struct', 'switch', 'this', 'throw',
            'true', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe',
            'ushort', 'using', 'virtual', 'void', 'volatile', 'while', 'async',
            'await', 'var', 'dynamic', 'get', 'set', 'add', 'remove', 'partial',
            'where', 'yield'
        ]

        for word in keywords:
            pattern = QtCore.QRegularExpression(r'\b' + word + r'\b')
            self.rules.append((pattern, keyword_format))

        # Strings
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor("#CE9178"))
        self.rules.append((QtCore.QRegularExpression(r'@"[^"]*"'), string_format))
        self.rules.append((QtCore.QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.rules.append((QtCore.QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # Comments
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor("#6A9955"))
        comment_format.setFontItalic(True)
        self.rules.append((QtCore.QRegularExpression(r'//[^\n]*'), comment_format))
        self.rules.append((QtCore.QRegularExpression(r'/\*.*?\*/'), comment_format))
        self.rules.append((QtCore.QRegularExpression(r'///[^\n]*'), comment_format))  # XML comments

        # Numbers
        number_format = QtGui.QTextCharFormat()
        number_format.setForeground(QtGui.QColor("#B5CEA8"))
        self.rules.append((QtCore.QRegularExpression(r'\b[0-9]+\b'), number_format))

# ------------------------------- Line number widget -------------------------------

class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.line_number_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

# ------------------------------- Code folding widget -------------------------------

class CodeFoldingArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(20, 0)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), QtGui.QColor("#252526"))

        block = self.editor.firstVisibleBlock()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and self.editor.is_foldable(block):
                painter.setPen(QtGui.QColor("#858585"))
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

# ------------------------------- Main editor widget -------------------------------

class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Font
        self.setFont(QtGui.QFont("Consolas", 12))
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setTabStopDistance(QtGui.QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)

        # Style
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                selection-background-color: #264f78;
            }
        """)

        # Highlighting (default Python)
        self.highlighter = PythonHighlighter(self.document())
        self.current_language = 'py'

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
        if ext == '.py':
            if self.current_language != 'py':
                self.highlighter = PythonHighlighter(self.document())
                self.current_language = 'py'
        elif ext in ('.c', '.cpp', '.h', '.hpp', '.cc', '.cxx'):
            if self.current_language != 'c':
                self.highlighter = CHighlighter(self.document())
                self.current_language = 'c'
        elif ext == '.cs':
            if self.current_language != 'cs':
                self.highlighter = CSharpHighlighter(self.document())
                self.current_language = 'cs'
        else:
            if self.current_language != 'none':
                self.highlighter = None
                self.current_language = 'none'
        if self.highlighter:
            self.highlighter.rehighlight()

    def is_foldable(self, block):
        text = block.text().strip()
        if self.current_language == 'py':
            return (text.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'with '))
                    and text.endswith(':'))
        elif self.current_language in ('c', 'cs'):
            return text.endswith('{') or (text.startswith(('#if', '#ifdef', '#ifndef')) and not text.endswith('#'))
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
        painter.fillRect(event.rect(), QtGui.QColor("#252526"))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtGui.QColor("#858585"))
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
            line_color = QtGui.QColor("#2a2a2a")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

# ------------------------------- Find/Replace dialog -------------------------------

class FindReplaceDialog(QtWidgets.QDialog):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Find and Replace")
        self.setModal(False)

        layout = QtWidgets.QVBoxLayout()

        find_layout = QtWidgets.QHBoxLayout()
        find_layout.addWidget(QtWidgets.QLabel("Find:"))
        self.find_input = QtWidgets.QLineEdit()
        self.find_input.setPlaceholderText("Text to find...")
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        replace_layout = QtWidgets.QHBoxLayout()
        replace_layout.addWidget(QtWidgets.QLabel("Replace:"))
        self.replace_input = QtWidgets.QLineEdit()
        self.replace_input.setPlaceholderText("Text to replace...")
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        options_layout = QtWidgets.QHBoxLayout()
        self.case_sensitive = QtWidgets.QCheckBox("Case sensitive")
        self.whole_words = QtWidgets.QCheckBox("Whole words")
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_words)
        layout.addLayout(options_layout)

        buttons_layout = QtWidgets.QHBoxLayout()
        self.find_next_btn = QtWidgets.QPushButton("Find Next")
        self.find_next_btn.clicked.connect(self.find_next)
        buttons_layout.addWidget(self.find_next_btn)
        self.find_prev_btn = QtWidgets.QPushButton("Find Previous")
        self.find_prev_btn.clicked.connect(self.find_previous)
        buttons_layout.addWidget(self.find_prev_btn)
        self.replace_btn = QtWidgets.QPushButton("Replace")
        self.replace_btn.clicked.connect(self.replace)
        buttons_layout.addWidget(self.replace_btn)
        self.replace_all_btn = QtWidgets.QPushButton("Replace All")
        self.replace_all_btn.clicked.connect(self.replace_all)
        buttons_layout.addWidget(self.replace_all_btn)
        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(self.close_btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def find_flags(self):
        flags = QtGui.QTextDocument.FindFlags()
        if self.case_sensitive.isChecked():
            flags |= QtGui.QTextDocument.FindCaseSensitively
        if self.whole_words.isChecked():
            flags |= QtGui.QTextDocument.FindWholeWords
        return flags

    def find_next(self):
        text = self.find_input.text()
        if text:
            found = self.editor.find(text, self.find_flags())
            if not found:
                cursor = self.editor.textCursor()
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
                self.editor.setTextCursor(cursor)
                found = self.editor.find(text, self.find_flags())
                if not found:
                    QtWidgets.QMessageBox.information(self, "Search", f"Text '{text}' not found")

    def find_previous(self):
        text = self.find_input.text()
        if text:
            flags = self.find_flags() | QtGui.QTextDocument.FindBackward
            found = self.editor.find(text, flags)
            if not found:
                cursor = self.editor.textCursor()
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
                self.editor.setTextCursor(cursor)
                found = self.editor.find(text, flags)
                if not found:
                    QtWidgets.QMessageBox.information(self, "Search", f"Text '{text}' not found")

    def replace(self):
        if not self.editor.textCursor().hasSelection():
            self.find_next()
        if self.editor.textCursor().hasSelection():
            self.editor.textCursor().insertText(self.replace_input.text())
            self.find_next()

    def replace_all(self):
        text = self.find_input.text()
        replace_text = self.replace_input.text()
        if not text:
            return
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
        self.editor.setTextCursor(cursor)
        count = 0
        while self.editor.find(text, self.find_flags()):
            self.editor.textCursor().insertText(replace_text)
            count += 1
        cursor.endEditBlock()
        QtWidgets.QMessageBox.information(self, "Replace", f"Replaced {count} occurrences")

# ------------------------------- Tab widget -------------------------------

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        self.new_tab_btn = QtWidgets.QToolButton()
        self.new_tab_btn.setText("+")
        self.new_tab_btn.clicked.connect(self.new_tab)
        self.setCornerWidget(self.new_tab_btn, QtCore.Qt.TopRightCorner)

        self.parent = parent

    def new_tab(self, file_path=None):
        editor = CodeEditor()
        if file_path and os.path.exists(file_path):
            editor.load_file(file_path)
            tab_name = os.path.basename(file_path)
        else:
            tab_name = "Untitled"
        index = self.addTab(editor, tab_name)
        self.setCurrentIndex(index)
        editor.document().modificationChanged.connect(
            lambda modified, idx=index: self.update_tab_title(idx, modified))
        return editor

    def update_tab_title(self, index, modified):
        editor = self.widget(index)
        if editor.file_path:
            title = os.path.basename(editor.file_path)
        else:
            title = "Untitled"
        if modified:
            title = "*" + title
        self.setTabText(index, title)

    def close_tab(self, index):
        editor = self.widget(index)
        if editor.is_modified:
            reply = QtWidgets.QMessageBox.question(
                self, "Save file",
                f"File '{self.tabText(index)}' has been modified. Save?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
            )
            if reply == QtWidgets.QMessageBox.Yes:
                if not self.parent.save_current_file():
                    return
            elif reply == QtWidgets.QMessageBox.Cancel:
                return
        self.removeTab(index)
        editor.deleteLater()

# ------------------------------- File tree dock widget -------------------------------

class FileTreeDock(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super().__init__("File Tree", parent)
        self.parent = parent
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        self.tree_view = QtWidgets.QTreeView()
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
        self.tree_view.setModel(self.model)
        self.set_root_to_current_dir()

        # Hide size, type, date columns
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        self.tree_view.doubleClicked.connect(self.on_file_double_clicked)
        self.tree_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

        self.setWidget(self.tree_view)

    def set_root_to_current_dir(self):
        """Set tree root to current working directory"""
        current_dir = QtCore.QDir.currentPath()
        self.tree_view.setRootIndex(self.model.index(current_dir))

    def set_root(self, path):
        """Set tree root to given path"""
        if os.path.isdir(path):
            self.tree_view.setRootIndex(self.model.index(path))

    def on_file_double_clicked(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.parent.open_file_from_path(path)

    def show_context_menu(self, position):
        index = self.tree_view.indexAt(position)
        if not index.isValid():
            return
        path = self.model.filePath(index)
        menu = QtWidgets.QMenu()
        if os.path.isdir(path):
            open_folder_action = menu.addAction("Open as Root")
            open_folder_action.triggered.connect(lambda: self.set_root(path))
        menu.exec(self.tree_view.viewport().mapToGlobal(position))

# ------------------------------- Main window -------------------------------

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CodeCast Editor")
        self.setGeometry(100, 100, 1200, 800)

        # Tab widget
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.new_tab()

        self.current_editor = None

        # File tree dock
        self.file_tree_dock = FileTreeDock(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.file_tree_dock)
        # Show file tree by default
        self.file_tree_dock.show()

        # Menus
        self.create_menus()

        # Status bar
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

        self.cursor_label = QtWidgets.QLabel("Line: 1, Col: 1")
        self.status_bar.addPermanentWidget(self.cursor_label)

        self.lines_label = QtWidgets.QLabel("Lines: 1")
        self.status_bar.addPermanentWidget(self.lines_label)

        # Autosave timer
        self.auto_save_timer = QtCore.QTimer()
        self.auto_save_timer.setInterval(30000)
        self.auto_save_timer.timeout.connect(self.auto_save_all)
        self.auto_save_timer.start()

        self.update_editor_connections()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def get_current_editor(self):
        return self.tab_widget.currentWidget()

    def update_editor_connections(self):
        editor = self.get_current_editor()
        if editor == self.current_editor:
            return
        # Отключаем сигналы от предыдущего редактора
        if self.current_editor is not None:
            try:
                self.current_editor.cursorPositionChanged.disconnect()
            except (TypeError, RuntimeError):
                pass
            try:
                self.current_editor.blockCountChanged.disconnect()
            except (TypeError, RuntimeError):
                pass
            try:
                self.current_editor.textChanged.disconnect()
            except (TypeError, RuntimeError):
                pass
        # Подключаем сигналы нового редактора
        if editor:
            editor.cursorPositionChanged.connect(self.update_cursor_position)
            editor.blockCountChanged.connect(self.update_line_count)
            editor.textChanged.connect(self.update_window_title)
        self.current_editor = editor

    def on_tab_changed(self, index):
        self.update_editor_connections()
        self.update_cursor_position()
        self.update_line_count()
        self.update_window_title()

    def update_cursor_position(self):
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            column = cursor.columnNumber() + 1
            self.cursor_label.setText(f"Line: {line}, Col: {column}")

    def update_line_count(self):
        editor = self.get_current_editor()
        if editor:
            lines = editor.blockCount()
            self.lines_label.setText(f"Lines: {lines}")

    def update_window_title(self):
        editor = self.get_current_editor()
        if editor:
            if editor.file_path:
                title = f"CodeCast - {os.path.basename(editor.file_path)}"
            else:
                title = "CodeCast - Untitled"
            if editor.is_modified:
                title = "*" + title
            self.setWindowTitle(title)

    def create_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        new_action = QtGui.QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QtGui.QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        open_root_action = QtGui.QAction("Open Folder as Root...", self)
        open_root_action.setShortcut("Ctrl+R")
        open_root_action.triggered.connect(self.choose_and_set_root)
        file_menu.addAction(open_root_action)

        file_menu.addSeparator()

        save_action = QtGui.QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_current_file)
        file_menu.addAction(save_action)

        save_as_action = QtGui.QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        save_all_action = QtGui.QAction("Save All", self)
        save_all_action.setShortcut("Ctrl+Alt+S")
        save_all_action.triggered.connect(self.save_all_files)
        file_menu.addAction(save_all_action)

        file_menu.addSeparator()

        close_tab_action = QtGui.QAction("Close Tab", self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(lambda: self.tab_widget.close_tab(self.tab_widget.currentIndex()))
        file_menu.addAction(close_tab_action)

        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        undo_action = QtGui.QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(lambda: self.get_current_editor().undo())
        edit_menu.addAction(undo_action)

        redo_action = QtGui.QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(lambda: self.get_current_editor().redo())
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QtGui.QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(lambda: self.get_current_editor().cut())
        edit_menu.addAction(cut_action)

        copy_action = QtGui.QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(lambda: self.get_current_editor().copy())
        edit_menu.addAction(copy_action)

        paste_action = QtGui.QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(lambda: self.get_current_editor().paste())
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        indent_action = QtGui.QAction("Increase Indent", self)
        indent_action.setShortcut("Tab")
        indent_action.triggered.connect(lambda: self.indent_selection())
        edit_menu.addAction(indent_action)

        unindent_action = QtGui.QAction("Decrease Indent", self)
        unindent_action.setShortcut("Shift+Tab")
        unindent_action.triggered.connect(lambda: self.unindent_selection())
        edit_menu.addAction(unindent_action)

        # Search menu
        search_menu = menubar.addMenu("Search")
        find_action = QtGui.QAction("Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.show_find_dialog)
        search_menu.addAction(find_action)

        replace_action = QtGui.QAction("Replace...", self)
        replace_action.setShortcut("Ctrl+H")
        replace_action.triggered.connect(self.show_replace_dialog)
        search_menu.addAction(replace_action)

        find_next_action = QtGui.QAction("Find Next", self)
        find_next_action.setShortcut("F3")
        find_next_action.triggered.connect(self.find_next)
        search_menu.addAction(find_next_action)

        find_prev_action = QtGui.QAction("Find Previous", self)
        find_prev_action.setShortcut("Shift+F3")
        find_prev_action.triggered.connect(self.find_previous)
        search_menu.addAction(find_prev_action)

        # View menu
        view_menu = menubar.addMenu("View")
        fold_all_action = QtGui.QAction("Fold All", self)
        fold_all_action.triggered.connect(self.fold_all)
        view_menu.addAction(fold_all_action)

        unfold_all_action = QtGui.QAction("Unfold All", self)
        unfold_all_action.triggered.connect(self.unfold_all)
        view_menu.addAction(unfold_all_action)

        view_menu.addSeparator()

        self.toggle_file_tree_action = QtGui.QAction("File Tree", self)
        self.toggle_file_tree_action.setCheckable(True)
        self.toggle_file_tree_action.setChecked(True)  # Visible by default
        self.toggle_file_tree_action.triggered.connect(self.toggle_file_tree)
        self.toggle_file_tree_action.setShortcut("Ctrl+Shift+F")
        view_menu.addAction(self.toggle_file_tree_action)

    def new_file(self):
        self.tab_widget.new_tab()

    def open_file(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Open files", "", "Python (*.py);;C/C++ (*.c *.cpp *.h *.hpp);;C# (*.cs);;All Files (*)")
        for file_path in file_paths:
            self.tab_widget.new_tab(file_path)

    def open_file_from_path(self, file_path):
        """Open a file from a path (e.g., from file tree)"""
        # Optionally check if already opened in a tab
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.file_path == file_path:
                self.tab_widget.setCurrentIndex(i)
                return
        # Otherwise open new tab
        self.tab_widget.new_tab(file_path)

    def choose_and_set_root(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Root Folder")
        if folder:
            self.file_tree_dock.set_root(folder)

    def save_current_file(self):
        editor = self.get_current_editor()
        if not editor:
            return False
        if editor.file_path:
            return editor.save_file(editor.file_path)
        else:
            return self.save_file_as()

    def save_file_as(self):
        editor = self.get_current_editor()
        if not editor:
            return False
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", "", "Python (*.py);;C/C++ (*.c *.cpp *.h);;C# (*.cs);;All Files (*)")
        if file_path:
            if not os.path.splitext(file_path)[1]:
                file_path += '.txt'
            if editor.save_file(file_path):
                editor.file_path = file_path
                editor.set_language_from_file(file_path)
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), os.path.basename(file_path))
                self.update_window_title()
                return True
        return False

    def save_all_files(self):
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.is_modified:
                if editor.file_path:
                    editor.save_file(editor.file_path)
                else:
                    self.tab_widget.setCurrentIndex(i)
                    self.save_file_as()

    def auto_save_all(self):
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.is_modified and editor.file_path:
                editor.save_file(editor.file_path)

    def show_find_dialog(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.show()

    def show_replace_dialog(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.replace_input.setEnabled(True)
        dialog.replace_btn.setEnabled(True)
        dialog.replace_all_btn.setEnabled(True)
        dialog.show()

    def find_next(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.find_next()

    def find_previous(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.find_previous()

    def indent_selection(self):
        editor = self.get_current_editor()
        if editor:
            editor.indent_selection()

    def unindent_selection(self):
        editor = self.get_current_editor()
        if editor:
            editor.unindent_selection()

    def fold_all(self):
        editor = self.get_current_editor()
        if editor:
            block = editor.document().begin()
            while block.isValid():
                if editor.is_foldable(block):
                    editor.toggle_fold(block)
                block = block.next()

    def unfold_all(self):
        editor = self.get_current_editor()
        if editor:
            editor.folded_blocks.clear()
            block = editor.document().begin()
            while block.isValid():
                block.setVisible(True)
                block = block.next()
            editor.folding_area.update()
            editor.line_number_area.update()

    def toggle_file_tree(self, checked=None):
        if checked is None:
            checked = self.toggle_file_tree_action.isChecked()
        if checked:
            self.file_tree_dock.show()
        else:
            self.file_tree_dock.hide()
        self.toggle_file_tree_action.setChecked(checked)

    def run_code(self):
        editor = self.get_current_editor()
        if not editor:
            return
        code = editor.toPlainText()
        output_dialog = QtWidgets.QDialog(self)
        output_dialog.setWindowTitle("Execution Result")
        output_dialog.setGeometry(200, 200, 600, 400)
        layout = QtWidgets.QVBoxLayout(output_dialog)
        output_text = QtWidgets.QTextEdit()
        output_text.setReadOnly(True)
        output_text.setFont(QtGui.QFont("Consolas", 10))
        layout.addWidget(output_text)
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(output_dialog.close)
        layout.addWidget(close_button)

        from io import StringIO
        import sys
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output
        try:
            exec(code)
            output = redirected_output.getvalue()
            if output:
                output_text.setPlainText(output)
            else:
                output_text.setPlainText("Code executed successfully (no output)")
        except Exception as e:
            output_text.setPlainText(f"Execution error:\n{str(e)}")
        finally:
            sys.stdout = old_stdout
        output_dialog.exec()

    def closeEvent(self, event):
        unsaved = []
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.is_modified:
                unsaved.append(i)
        if unsaved:
            reply = QtWidgets.QMessageBox.question(
                self, "Unsaved changes",
                f"There are {len(unsaved)} files with unsaved changes. Save all?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.save_all_files()
                event.accept()
            elif reply == QtWidgets.QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()

# ------------------------------- Launch -------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(dark_palette)

    window = MainApplication()
    window.show()
    sys.exit(app.exec())