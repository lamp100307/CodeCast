from PySide6 import QtWidgets, QtCore, QtGui

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