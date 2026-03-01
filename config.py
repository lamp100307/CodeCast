import os
from pathlib import Path

APP_DIR = Path.home() / ".codecast"
THEMES_DIR = APP_DIR / "themes"
CONFIG_FILE = APP_DIR / "config.json"
EXTENSIONS_DIR = APP_DIR / "extensions"

# Базовая тема "Dark" (расширенная, с UI цветами)
BASE_THEMES = {
    "dark.json": {
        "name": "Dark",
        "colors": {
            "background": "#1e1e1e",
            "foreground": "#d4d4d4",
            "selection": "#264f78",
            "lineHighlight": "#2a2a2a",
            "lineNumbers": "#858585",
            "fold": "#1e1e1e",
            "keyword": "#569CD6",
            "string": "#CE9178",
            "comment": "#6A9955",
            "function": "#DCDCAA",
            "decorator": "#D7BA7D",
            "number": "#B5CEA8",
            "preprocessor": "#D7BA7D"
        },
        "ui": {
            "window": "#2d2d2d",
            "windowText": "#ffffff",
            "base": "#1e1e1e",
            "alternateBase": "#2d2d2d",
            "text": "#ffffff",
            "button": "#3c3c3c",
            "buttonText": "#ffffff",
            "brightText": "#ff0000",
            "link": "#2a82da",
            "highlight": "#2a82da",
            "highlightedText": "#000000",
            "toolTipBase": "#ffffff",
            "toolTipText": "#000000"
        }
    },
    "light.json": {
        "name": "Light",
        "colors": {
            "background": "#ffffff",
            "foreground": "#000000",
            "selection": "#add6ff",
            "lineHighlight": "#f0f0f0",
            "lineNumbers": "#237893",
            "fold": "#ffffff",
            "keyword": "#0000ff",
            "string": "#a31515",
            "comment": "#008000",
            "function": "#795e26",
            "decorator": "#af00db",
            "number": "#098658",
            "preprocessor": "#af00db"
        },
        "ui": {
            "window": "#f0f0f0",
            "windowText": "#000000",
            "base": "#ffffff",
            "alternateBase": "#f0f0f0",
            "text": "#000000",
            "button": "#e0e0e0",
            "buttonText": "#000000",
            "brightText": "#ff0000",
            "link": "#0000ff",
            "highlight": "#3399ff",
            "highlightedText": "#ffffff",
            "toolTipBase": "#ffffdc",
            "toolTipText": "#000000"
        }
    }
}

# Базовые расширения (синтаксис)
BASE_EXTENSIONS = {
    "python": {
        "fileExtension": ".py",
        "displayName": "Python",
        "rules": [
            {"ruleName": "keyword", "regex": r"\b(?:and|assert|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|not|or|pass|print|raise|return|try|while|with|yield|None|True|False|as|async|await)\b"},
            {"ruleName": "string", "regex": r'"[^"\\]*(\\.[^"\\]*)*"'},
            {"ruleName": "string", "regex": r"'[^'\\]*(\\.[^'\\]*)*'"},
            {"ruleName": "comment", "regex": r"#[^\n]*"},
            {"ruleName": "function", "regex": r"\b[A-Za-z0-9_]+(?=\()"},
            {"ruleName": "decorator", "regex": r"^\s*@[A-Za-z_][A-Za-z0-9_]*"},
            {"ruleName": "number", "regex": r"\b[0-9]+\b"}
        ]
    },
    "c_cpp": {
        "fileExtension": [".c", ".cpp", ".h", ".hpp", ".cc", ".cxx"],
        "displayName": "C/C++",
        "rules": [
            {"ruleName": "keyword", "regex": r"\b(?:auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|class|private|protected|public|namespace|using|this|new|delete|throw|try|catch|virtual|override|final|friend|operator|template|typename|explicit|static_cast|dynamic_cast|const_cast|reinterpret_cast|bool|true|false)\b"},
            {"ruleName": "string", "regex": r'"[^"\\]*(\\.[^"\\]*)*"'},
            {"ruleName": "string", "regex": r"'[^'\\]*(\\.[^'\\]*)*'"},
            {"ruleName": "comment", "regex": r"//[^\n]*"},
            {"ruleName": "comment", "regex": r"/\*.*?\*/"},
            {"ruleName": "preprocessor", "regex": r"^\s*#\s*[a-zA-Z]+"},
            {"ruleName": "number", "regex": r"\b[0-9]+\b"},
            {"ruleName": "number", "regex": r"\b0x[0-9a-fA-F]+\b"}
        ]
    },
    "csharp": {
        "fileExtension": ".cs",
        "displayName": "C#",
        "rules": [
            {"ruleName": "keyword", "regex": r"\b(?:abstract|as|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|do|double|else|enum|event|explicit|extern|false|finally|fixed|float|for|foreach|goto|if|implicit|in|int|interface|internal|is|lock|long|namespace|new|null|object|operator|out|override|params|private|protected|public|readonly|ref|return|sbyte|sealed|short|sizeof|stackalloc|static|string|struct|switch|this|throw|true|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|virtual|void|volatile|while|async|await|var|dynamic|get|set|add|remove|partial|where|yield)\b"},
            {"ruleName": "string", "regex": r'@"[^"]*"'},
            {"ruleName": "string", "regex": r'"[^"\\]*(\\.[^"\\]*)*"'},
            {"ruleName": "string", "regex": r"'[^'\\]*(\\.[^'\\]*)*'"},
            {"ruleName": "comment", "regex": r"//[^\n]*"},
            {"ruleName": "comment", "regex": r"/\*.*?\*/"},
            {"ruleName": "comment", "regex": r"///[^\n]*"},
            {"ruleName": "number", "regex": r"\b[0-9]+\b"}
        ]
    }
}