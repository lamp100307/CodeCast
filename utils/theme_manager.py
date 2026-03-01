from PySide6 import QtGui, QtCore
from config import THEMES_DIR, BASE_THEMES
import json

class ThemeManager(QtCore.QObject):
    """Менеджер тем с поддержкой сигналов об изменениях"""
    
    theme_changed = QtCore.Signal(str)  # имя новой темы
    themes_updated = QtCore.Signal()    # список тем обновлён
    
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.themes = {}
        self.current_theme = None
        self.load_themes()

    def load_themes(self):
        """Загружает все темы из папки"""
        THEMES_DIR.mkdir(parents=True, exist_ok=True)
        
        # Создаём базовые темы, если их нет
        for name, data in BASE_THEMES.items():
            theme_path = THEMES_DIR / name
            if not theme_path.exists():
                with open(theme_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

        # Загружаем все темы из папки
        old_themes = set(self.themes.keys())
        self.themes.clear()
        
        for theme_file in THEMES_DIR.glob("*.json"):
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    theme_name = data.get("name", theme_file.stem)
                    self.themes[theme_name] = data
            except Exception as e:
                print(f"Error loading theme {theme_file}: {e}")
        
        # Проверяем, изменился ли список тем
        new_themes = set(self.themes.keys())
        if old_themes != new_themes:
            self.themes_updated.emit()

        # Устанавливаем тему из конфига
        saved_theme = self.config.get("theme", "Dark")
        if saved_theme in self.themes:
            self.set_theme(saved_theme, save_to_config=False)
        elif self.themes:
            first_theme = list(self.themes.keys())[0]
            self.set_theme(first_theme, save_to_config=False)

    def get_color(self, key, default="#000000"):
        """Возвращает цвет из текущей темы"""
        if self.current_theme and "colors" in self.current_theme:
            return self.current_theme["colors"].get(key, default)
        return default

    def get_ui_color(self, key, default="#000000"):
        """Возвращает UI цвет из текущей темы"""
        if self.current_theme and "ui" in self.current_theme:
            return self.current_theme["ui"].get(key, default)
        return default

    def set_theme(self, theme_name, save_to_config=True):
        """Устанавливает тему по имени"""
        if theme_name in self.themes:
            old_theme = self.current_theme.get("name") if self.current_theme else None
            self.current_theme = self.themes[theme_name]
            
            if save_to_config:
                self.config.set("theme", theme_name)
            
            # Если тема действительно изменилась, испускаем сигнал
            if old_theme != theme_name:
                self.theme_changed.emit(theme_name)
            return True
        return False

    def get_theme_names(self):
        """Возвращает список доступных тем"""
        return list(self.themes.keys())

    def apply_theme_to_app(self, app):
        """Применяет UI цвета темы к приложению через палитру"""
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(self.get_ui_color("window", "#2d2d2d")))
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(self.get_ui_color("windowText", "#ffffff")))
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(self.get_ui_color("base", "#1e1e1e")))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(self.get_ui_color("alternateBase", "#2d2d2d")))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(self.get_ui_color("text", "#ffffff")))
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(self.get_ui_color("button", "#3c3c3c")))
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(self.get_ui_color("buttonText", "#ffffff")))
        palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(self.get_ui_color("brightText", "#ff0000")))
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(self.get_ui_color("link", "#2a82da")))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(self.get_ui_color("highlight", "#2a82da")))
        palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(self.get_ui_color("highlightedText", "#000000")))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(self.get_ui_color("toolTipBase", "#ffffff")))
        palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(self.get_ui_color("toolTipText", "#000000")))
        app.setPalette(palette)