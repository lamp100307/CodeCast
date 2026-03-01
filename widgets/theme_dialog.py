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
        layout.addWidget(self.list_widget)

        # Кнопка обновления
        refresh_btn = QtWidgets.QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_themes)

        button_box = QtWidgets.QDialogButtonBox()
        button_box.addButton(refresh_btn, QtWidgets.QDialogButtonBox.ActionRole)
        button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        button_box.addButton(QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Подключаем сигнал обновления от менеджера
        self.theme_manager.themes_updated.connect(self.refresh_themes)

        self.refresh_themes()

    def refresh_themes(self):
        """Обновляет список тем"""
        current_item = self.list_widget.currentItem()
        current_text = current_item.text() if current_item else None
        
        self.list_widget.clear()
        self.list_widget.addItems(self.theme_manager.get_theme_names())
        
        # Восстанавливаем выделение
        if current_text:
            items = self.list_widget.findItems(current_text, QtCore.Qt.MatchExactly)
            if items:
                self.list_widget.setCurrentItem(items[0])
        else:
            # Highlight current theme
            current_name = self.theme_manager.current_theme.get("name") if self.theme_manager.current_theme else None
            if current_name:
                items = self.list_widget.findItems(current_name, QtCore.Qt.MatchExactly)
                if items:
                    self.list_widget.setCurrentItem(items[0])

    def get_selected_theme(self):
        item = self.list_widget.currentItem()
        return item.text() if item else None