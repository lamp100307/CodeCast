from config import EXTENSIONS_DIR, BASE_EXTENSIONS
from .extension_highlighter import ExtensionHighlighter
from PySide6 import QtCore
import json
import os

class ExtensionManager(QtCore.QObject):
    """Менеджер расширений с поддержкой сигналов об изменениях"""
    
    extensions_updated = QtCore.Signal()  # список расширений обновлён
    extension_enabled_changed = QtCore.Signal(str, bool)  # имя, включено
    
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.extensions = {}  # key: file extension -> syntax data
        self.extension_info = {}  # key: extension name -> project info
        self.extension_dir_names = {}  # key: extension name -> directory name
        self.language_names = {}
        self.load_extensions()

    def load_extensions(self):
        """Загружает все расширения из папки"""
        EXTENSIONS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Создаём базовые расширения, если их нет
        for lang, data in BASE_EXTENSIONS.items():
            ext_dir = EXTENSIONS_DIR / lang
            if not ext_dir.exists():
                ext_dir.mkdir()
                # project.json
                project_data = {
                    "name": f"{data['displayName']} Support",
                    "version": "0.1.0",
                    "type": "syntax",
                    "description": f"Built-in {data['displayName']} syntax",
                    "developers": ["CodeCast"],
                    "enabled": True
                }
                with open(ext_dir / "project.json", 'w', encoding='utf-8') as f:
                    json.dump(project_data, f, indent=4)
                # syntaxhighlighter.json
                syntax_data = {
                    "fileExtension": data["fileExtension"],
                    "displayName": data["displayName"],
                    "rules": data["rules"]
                }
                with open(ext_dir / "syntaxhighlighter.json", 'w', encoding='utf-8') as f:
                    json.dump(syntax_data, f, indent=4)

        # Загружаем все расширения
        old_extensions = set(self.extension_info.keys())
        self.extensions.clear()
        self.extension_info.clear()
        self.extension_dir_names.clear()
        self.language_names.clear()
        
        for ext_dir in EXTENSIONS_DIR.iterdir():
            if ext_dir.is_dir():
                project_file = ext_dir / "project.json"
                syntax_file = ext_dir / "syntaxhighlighter.json"
                dir_name = ext_dir.name
                
                # Загружаем информацию о расширении
                if project_file.exists():
                    try:
                        with open(project_file, 'r', encoding='utf-8') as f:
                            project_data = json.load(f)
                            ext_name = project_data.get("name", dir_name)
                            self.extension_info[ext_name] = project_data
                            self.extension_dir_names[ext_name] = dir_name
                    except Exception as e:
                        print(f"Error loading project info {ext_dir}: {e}")
                else:
                    # Если нет project.json, используем имя папки
                    ext_name = dir_name
                    self.extension_info[ext_name] = {
                        "name": ext_name,
                        "version": "0.0.0",
                        "description": "",
                        "developers": []
                    }
                    self.extension_dir_names[ext_name] = dir_name

        # Второй проход: загружаем синтаксис для включенных расширений
        for ext_name, ext_info in self.extension_info.items():
            dir_name = self.extension_dir_names[ext_name]
            syntax_file = EXTENSIONS_DIR / dir_name / "syntaxhighlighter.json"
            
            # Загружаем синтаксис (только если расширение включено)
            if syntax_file.exists() and self._is_extension_enabled(ext_name):
                try:
                    with open(syntax_file, 'r', encoding='utf-8') as f:
                        syntax_data = json.load(f)
                    extensions_list = syntax_data.get("fileExtension", [])
                    if isinstance(extensions_list, str):
                        extensions_list = [extensions_list]
                    for ext in extensions_list:
                        self.extensions[ext] = syntax_data
                        self.language_names[ext] = syntax_data.get("displayName", ext)
                except Exception as e:
                    print(f"Error loading syntax {syntax_file}: {e}")

        # Проверяем, изменился ли список расширений
        new_extensions = set(self.extension_info.keys())
        if old_extensions != new_extensions:
            self.extensions_updated.emit()

    def _is_extension_enabled(self, ext_name):
        """Проверяет, включено ли расширение в конфиге"""
        return self.config.is_extension_enabled(ext_name)

    def get_highlighter_for_file(self, file_path, theme_manager):
        """Возвращает подсветку для файла"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.extensions:
            return ExtensionHighlighter(self.extensions[ext], theme_manager, parent=None)
        return None

    def get_all_extensions_info(self):
        """Возвращает информацию обо всех установленных расширениях"""
        return self.extension_info

    def set_extension_enabled(self, ext_name, enabled):
        """Включает/отключает расширение"""
        self.config.set_extension_enabled(ext_name, enabled)
        self.extension_enabled_changed.emit(ext_name, enabled)
        # Перезагружаем расширения
        self.load_extensions()

    def reload_extensions(self):
        """Перезагружает расширения (после включения/отключения)"""
        self.load_extensions()