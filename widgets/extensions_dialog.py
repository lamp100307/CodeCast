from PySide6 import QtWidgets, QtCore, QtGui

class ExtensionsDialog(QtWidgets.QDialog):
    def __init__(self, extension_manager, parent=None):
        super().__init__(parent)
        self.extension_manager = extension_manager
        self.setWindowTitle("Extensions Manager")
        self.setModal(True)
        self.setMinimumSize(600, 400)

        layout = QtWidgets.QVBoxLayout(self)

        # Таблица расширений
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Enabled", "Name", "Version", "Description", "Developers"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)

        # Кнопка обновления
        refresh_btn = QtWidgets.QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_extensions)

        # Кнопки OK/Cancel
        button_box = QtWidgets.QDialogButtonBox()
        button_box.addButton(refresh_btn, QtWidgets.QDialogButtonBox.ActionRole)
        button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        button_box.addButton(QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)

        # Подключаем сигнал обновления от менеджера
        self.extension_manager.extensions_updated.connect(self.refresh_extensions)

        self.load_extensions()

    def load_extensions(self):
        """Загружает список расширений в таблицу"""
        extensions = self.extension_manager.get_all_extensions_info()
        self.table.setRowCount(len(extensions))

        for row, (ext_name, ext_info) in enumerate(extensions.items()):
            # Чекбокс для включения/отключения
            enabled = self.extension_manager.config.is_extension_enabled(ext_name)
            cb = QtWidgets.QCheckBox()
            cb.setChecked(enabled)
            cb.stateChanged.connect(lambda state, name=ext_name: self.on_enable_changed(name, state))
            
            cell_widget = QtWidgets.QWidget()
            cell_layout = QtWidgets.QHBoxLayout(cell_widget)
            cell_layout.addWidget(cb)
            cell_layout.setAlignment(QtCore.Qt.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            
            self.table.setCellWidget(row, 0, cell_widget)

            # Название
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(ext_info.get("name", ext_name)))

            # Версия
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(ext_info.get("version", "0.0.0")))

            # Описание
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(ext_info.get("description", "")))

            # Разработчики
            developers = ext_info.get("developers", [])
            if isinstance(developers, list):
                dev_text = ", ".join(developers)
            else:
                dev_text = str(developers)
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(dev_text))

        self.table.resizeColumnsToContents()

    def refresh_extensions(self):
        """Обновляет таблицу"""
        # Сохраняем текущую прокрутку
        scroll_pos = self.table.verticalScrollBar().value()
        
        self.table.clearContents()
        self.load_extensions()
        
        # Восстанавливаем прокрутку
        self.table.verticalScrollBar().setValue(scroll_pos)

    def on_enable_changed(self, ext_name, state):
        """Обработчик изменения состояния чекбокса"""
        enabled = state == 2
        self.extension_manager.set_extension_enabled(ext_name, enabled)