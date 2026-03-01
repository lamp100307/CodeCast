from config import EXTENSIONS_DIR, BASE_EXTENSIONS
from .extension_highlghter import ExtensionHighlighter
import json
import os

class ExtensionManager:
    def __init__(self):
        self.extensions = {}  # key: file extension (e.g. '.py') -> extension data
        self.language_names = {}  # extension -> display name
        self.load_extensions()

    def load_extensions(self):
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
                    "developers": ["CodeCast"]
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
        for ext_dir in EXTENSIONS_DIR.iterdir():
            if ext_dir.is_dir():
                syntax_file = ext_dir / "syntaxhighlighter.json"
                if syntax_file.exists():
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
                        print(f"Error loading extension {ext_dir}: {e}")

    def get_highlighter_for_file(self, file_path, theme_manager):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.extensions:
            return ExtensionHighlighter(self.extensions[ext], theme_manager, parent=None)
        return None