from PySide6 import QtWidgets, QtCore
from widgets.code_redactor import CodeEditor
import os

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, theme_manager, extension_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.extension_manager = extension_manager
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        self.new_tab_btn = QtWidgets.QToolButton()
        self.new_tab_btn.setText("+")
        self.new_tab_btn.clicked.connect(self.new_tab)
        self.setCornerWidget(self.new_tab_btn, QtCore.Qt.TopRightCorner)

        self.parent = parent

    def new_tab(self, file_path=None):
        editor = CodeEditor(self.theme_manager, self.extension_manager)
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