from PySide6 import QtCore
import os
from pathlib import Path

class FileSystemWatcher(QtCore.QObject):
    """Наблюдает за изменениями в папках тем и расширений"""
    
    themes_changed = QtCore.Signal()
    extensions_changed = QtCore.Signal()
    
    def __init__(self, themes_dir, extensions_dir, parent=None):
        super().__init__(parent)
        self.themes_dir = str(themes_dir)
        self.extensions_dir = str(extensions_dir)
        
        self.watcher = QtCore.QFileSystemWatcher(self)
        
        # Добавляем папки для отслеживания
        if os.path.exists(self.themes_dir):
            self.watcher.addPath(self.themes_dir)
        if os.path.exists(self.extensions_dir):
            self.watcher.addPath(self.extensions_dir)
        
        # Подключаем сигналы
        self.watcher.directoryChanged.connect(self.on_directory_changed)
        self.watcher.fileChanged.connect(self.on_file_changed)
        
        # Таймер для дебаунса (чтобы не реагировать на каждое мелкое изменение)
        self.debounce_timer = QtCore.QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.setInterval(500)  # 500 мс
        self.debounce_timer.timeout.connect(self.emit_changes)
        
        self.pending_themes = False
        self.pending_extensions = False
    
    def on_directory_changed(self, path):
        """Обработчик изменения директории"""
        if path == self.themes_dir:
            self.pending_themes = True
        elif path == self.extensions_dir:
            self.pending_extensions = True
        self.debounce_timer.start()
    
    def on_file_changed(self, path):
        """Обработчик изменения файла"""
        parent = str(Path(path).parent)
        if parent == self.themes_dir:
            self.pending_themes = True
        elif parent == self.extensions_dir:
            self.pending_extensions = True
        self.debounce_timer.start()
    
    def emit_changes(self):
        """Испускает сигналы после дебаунса"""
        if self.pending_themes:
            self.themes_changed.emit()
            self.pending_themes = False
        if self.pending_extensions:
            self.extensions_changed.emit()
            self.pending_extensions = False