from PySide6 import QtWidgets, QtCore

class ThemeDialog(QtWidgets.QDialog):
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setWindowTitle("Themes")
        self.setModal(True)
        self.setMinimumSize(400, 300)

        layout = QtWidgets.QVBoxLayout(self)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItems(self.theme_manager.get_theme_names())
        # Highlight current theme
        current_name = self.theme_manager.current_theme.get("name") if self.theme_manager.current_theme else None
        if current_name:
            items = self.list_widget.findItems(current_name, QtCore.Qt.MatchExactly)
            if items:
                self.list_widget.setCurrentItem(items[0])

        layout.addWidget(self.list_widget)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_selected_theme(self):
        item = self.list_widget.currentItem()
        return item.text() if item else None