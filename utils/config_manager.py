import json
from pathlib import Path
from config import APP_DIR, CONFIG_FILE

class ConfigManager:
    def __init__(self):
        self.config = self._default_config()
        self.config_file = CONFIG_FILE
        self.load()

    def _default_config(self):
        return {
            "theme": "Dark",
            "font_size": 12,
            "font_family": "Consolas",
            "auto_save_interval": 30,
            "show_line_numbers": True,
            "show_folding": True,
            "word_wrap": False,
            "tab_size": 4,
            "console_visible": False,
            "file_tree_visible": True,
            "recent_files": [],
            "extensions_enabled": {}  # для включения/отключения расширений
        }

    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Обновляем только существующие ключи, добавляя новые из дефолта
                    for key, value in loaded.items():
                        if key in self.config:
                            self.config[key] = value
                    print(f"Config loaded: {self.config}")  # отладка
            except Exception as e:
                print(f"Error loading config: {e}")
        else:
            # Если файла нет, создаём с дефолтными настройками
            self.save()

    def save(self):
        try:
            APP_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            print(f"Config saved: {self.config}")  # отладка
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()

    def add_recent_file(self, file_path):
        recent = self.config.get("recent_files", [])
        if file_path in recent:
            recent.remove(file_path)
        recent.insert(0, file_path)
        self.config["recent_files"] = recent[:10]
        self.save()

    def is_extension_enabled(self, ext_name):
        """Проверяет, включено ли расширение"""
        enabled = self.config.get("extensions_enabled", {}).get(ext_name, True)
        print(f"Checking if extension '{ext_name}' is enabled: {enabled}")  # отладка
        return enabled

    def set_extension_enabled(self, ext_name, enabled):
        """Включает/отключает расширение"""
        if "extensions_enabled" not in self.config:
            self.config["extensions_enabled"] = {}
        self.config["extensions_enabled"][ext_name] = enabled
        print(f"Extension '{ext_name}' set to {enabled}")  # отладка
        self.save()