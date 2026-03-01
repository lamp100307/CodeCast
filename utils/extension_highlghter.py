from PySide6 import QtCore, QtGui
import os

class ExtensionHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, syntax_data, theme_manager, parent=None):
        super().__init__(parent)
        self.syntax_data = syntax_data
        self.theme_manager = theme_manager
        self.rules = []
        self.load_rules()

    def load_rules(self):
        for rule in self.syntax_data.get("rules", []):
            rule_name = rule.get("ruleName")
            regex = rule.get("regex")
            if not regex:
                continue
            color = self.theme_manager.get_color(rule_name, "#000000")
            fmt = QtGui.QTextCharFormat()
            fmt.setForeground(QtGui.QColor(color))
            if rule_name == "comment":
                fmt.setFontItalic(True)
            elif rule_name == "keyword":
                fmt.setFontWeight(QtGui.QFont.Weight.Bold)
            # Добавляем правило
            pattern = QtCore.QRegularExpression(regex)
            self.rules.append((pattern, fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)