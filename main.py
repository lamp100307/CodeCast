import sys
from PySide6 import QtWidgets, QtCore, QtGui

class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        
    def sizeHint(self):
        return QtCore.QSize(self.editor.line_number_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class PythonHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        # Формат для ключевых слов
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor("#569CD6"))
        keyword_format.setFontWeight(QtGui.QFont.Weight.Bold)
        
        # Список ключевых слов Python
        keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'with', 'yield',
            'None', 'True', 'False', 'as', 'async', 'await'
        ]
        
        for word in keywords:
            pattern = QtCore.QRegularExpression(f'\\b{word}\\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Формат для строк
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor("#CE9178"))
        
        # Строки в кавычках
        self.highlighting_rules.append((
            QtCore.QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), 
            string_format
        ))
        self.highlighting_rules.append((
            QtCore.QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), 
            string_format
        ))
        
        # Формат для комментариев
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor("#6A9955"))
        comment_format.setFontItalic(True)
        
        self.highlighting_rules.append((
            QtCore.QRegularExpression("#[^\n]*"), 
            comment_format
        ))
        
        # Формат для функций
        function_format = QtGui.QTextCharFormat()
        function_format.setForeground(QtGui.QColor("#DCDCAA"))
        
        self.highlighting_rules.append((
            QtCore.QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"),
            function_format
        ))
        
        # Формат для декораторов
        decorator_format = QtGui.QTextCharFormat()
        decorator_format.setForeground(QtGui.QColor("#D7BA7D"))
        
        self.highlighting_rules.append((
            QtCore.QRegularExpression("^\\s*@[A-Za-z_][A-Za-z0-9_]*"),
            decorator_format
        ))
        
        # Формат для чисел
        number_format = QtGui.QTextCharFormat()
        number_format.setForeground(QtGui.QColor("#B5CEA8"))
        
        self.highlighting_rules.append((
            QtCore.QRegularExpression("\\b[0-9]+\\b"),
            number_format
        ))
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        
        # Настройка внешнего вида
        self.setFont(QtGui.QFont("Consolas", 12))
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setTabStopDistance(QtGui.QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)
        
        # Настройка цветовой схемы
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                selection-background-color: #264f78;
            }
        """)
        
        # Подсветка синтаксиса
        self.highlighter = PythonHighlighter(self.document())
        
        # Создаем виджет с номерами строк
        self.line_number_area = LineNumberArea(self)
        
        # Подключаем сигналы
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        self.update_line_number_area_width(0)
        self.highlight_current_line()
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Tab:
            # Автотабуляция
            cursor = self.textCursor()
            if cursor.hasSelection():
                # Если есть выделение, добавляем табуляцию в начало каждой строки
                self.indent_selection()
            else:
                # Иначе просто вставляем табуляцию
                super().keyPressEvent(event)
        elif event.key() == QtCore.Qt.Key.Key_Backtab:
            # Shift+Tab для удаления отступа
            self.unindent_selection()
        elif event.key() == QtCore.Qt.Key.Key_Return:
            # Автоматический отступ после Enter
            super().keyPressEvent(event)
            self.auto_indent()
        elif event.key() == QtCore.Qt.Key.Key_BraceLeft:
            # Автоматическое закрытие скобок
            super().keyPressEvent(event)
            self.textCursor().insertText('}')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        elif event.key() == QtCore.Qt.Key.Key_ParenLeft:
            super().keyPressEvent(event)
            self.textCursor().insertText(')')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        elif event.key() == QtCore.Qt.Key.Key_BracketLeft:
            super().keyPressEvent(event)
            self.textCursor().insertText(']')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        elif event.key() == QtCore.Qt.Key.Key_QuoteDbl:
            super().keyPressEvent(event)
            self.textCursor().insertText('"')
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Left)
        else:
            super().keyPressEvent(event)
    
    def indent_selection(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        
        while cursor.position() <= end:
            cursor.insertText('    ')
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextBlock)
            if cursor.atEnd():
                break
        
        cursor.endEditBlock()
    
    def unindent_selection(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
        
        while cursor.position() <= end:
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextCharacter, 
                              QtGui.QTextCursor.MoveMode.KeepAnchor, 4)
            if cursor.selectedText() == '    ':
                cursor.removeSelectedText()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextBlock)
            if cursor.atEnd():
                break
        
        cursor.endEditBlock()
    
    def auto_indent(self):
        cursor = self.textCursor()
        block = cursor.block()
        text = block.text()
        
        # Определяем отступ предыдущей строки
        indent = len(text) - len(text.lstrip())
        
        # Проверяем, нужно ли увеличить отступ (после двоеточия)
        if text.rstrip().endswith(':'):
            indent += 4
        
        # Добавляем отступ
        if indent > 0:
            cursor.insertText(' ' * indent)
    
    def line_number_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, new_block_count):
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QtCore.QRect(cr.left(), cr.top(), 
                                                      self.line_number_width(), cr.height()))
    
    def line_number_area_paint_event(self, event):
        painter = QtGui.QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QtGui.QColor("#252526"))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtGui.QColor("#858585"))
                painter.setFont(self.font())
                painter.drawText(0, int(top), self.line_number_area.width() - 2, 
                               self.fontMetrics().height(), QtCore.Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def highlight_current_line(self):
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = QtGui.QColor("#2a2a2a")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CodeCast - Python Editor")
        self.setGeometry(100, 100, 1000, 700)
        
        self.current_file = None
        
        # Сначала создаем редактор
        self.redactor_main_edit = CodeEditor()
        
        # Потом создаем тулбар (теперь редактор уже существует)
        self.create_toolbar()
        
        # Создаем меню
        self.create_menus()
        
        # Создаем центральный виджет
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Добавляем редактор в layout
        layout.addWidget(self.redactor_main_edit)
        
        # Статус бар
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
        
        # Устанавливаем начальный текст
        self.redactor_main_edit.setPlainText("""# Добро пожаловать в CodeCast!
# Python редактор с подсветкой синтаксиса

def hello_world():
    print("Привет, мир!")
    
    # Это комментарий
    numbers = [1, 2, 3, 4, 5]
    for i in numbers:
        if i % 2 == 0:
            print(f"Число {i} - четное")
        else:
            print(f"Число {i} - нечетное")
    
    return "Готово!"

class ExampleClass:
    def __init__(self, name):
        self.name = name
    
    @property
    def greeting(self):
        return f"Привет, {self.name}!"

if __name__ == "__main__":
    result = hello_world()
    print(result)
    
    obj = ExampleClass("Мир")
    print(obj.greeting)""")
        
        # Подключаем сигналы
        self.redactor_main_edit.cursorPositionChanged.connect(self.update_cursor_position)
        self.redactor_main_edit.textChanged.connect(self.update_status)
    
    def create_toolbar(self):
        toolbar = self.addToolBar("Инструменты")
        toolbar.setMovable(False)
        toolbar.setIconSize(QtCore.QSize(20, 20))
        
        # Действия для редактирования
        cut_action = QtGui.QAction("✂️ Вырезать", self)
        cut_action.triggered.connect(self.redactor_main_edit.cut)
        toolbar.addAction(cut_action)
        
        copy_action = QtGui.QAction("📋 Копировать", self)
        copy_action.triggered.connect(self.redactor_main_edit.copy)
        toolbar.addAction(copy_action)
        
        paste_action = QtGui.QAction("📋 Вставить", self)
        paste_action.triggered.connect(self.redactor_main_edit.paste)
        toolbar.addAction(paste_action)
        
        toolbar.addSeparator()
        
        # Действия для форматирования
        undo_action = QtGui.QAction("↩️ Отменить", self)
        undo_action.triggered.connect(self.redactor_main_edit.undo)
        toolbar.addAction(undo_action)
        
        redo_action = QtGui.QAction("↪️ Повторить", self)
        redo_action.triggered.connect(self.redactor_main_edit.redo)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        # Поиск
        search_action = QtGui.QAction("🔍 Поиск", self)
        search_action.triggered.connect(self.search_text)
        toolbar.addAction(search_action)
        
        # Запуск
        run_action = QtGui.QAction("▶️ Запустить", self)
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)
    
    def create_menus(self):
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        new_action = QtGui.QAction("Новый", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QtGui.QAction("Открыть...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QtGui.QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QtGui.QAction("Сохранить как...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QtGui.QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню Правка
        edit_menu = menubar.addMenu("Правка")
        
        undo_action = QtGui.QAction("Отменить", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.redactor_main_edit.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QtGui.QAction("Повторить", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redactor_main_edit.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QtGui.QAction("Вырезать", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.redactor_main_edit.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QtGui.QAction("Копировать", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.redactor_main_edit.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QtGui.QAction("Вставить", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.redactor_main_edit.paste)
        edit_menu.addAction(paste_action)
        
        # Меню Поиск
        search_menu = menubar.addMenu("Поиск")
        
        find_action = QtGui.QAction("Найти...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.search_text)
        search_menu.addAction(find_action)
    
    def new_file(self):
        self.redactor_main_edit.clear()
        self.current_file = None
        self.setWindowTitle("CodeCast - Новый файл")
        self.status_bar.showMessage("Новый файл создан")
    
    def open_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Python Files (*.py);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.redactor_main_edit.setPlainText(file.read())
                self.current_file = file_name
                self.setWindowTitle(f"CodeCast - {file_name}")
                self.status_bar.showMessage(f"Файл {file_name} открыт")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.redactor_main_edit.toPlainText())
                self.status_bar.showMessage(f"Файл {self.current_file} сохранен")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Python Files (*.py);;All Files (*)")
        if file_name:
            if not file_name.endswith('.py'):
                file_name += '.py'
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(self.redactor_main_edit.toPlainText())
                self.current_file = file_name
                self.setWindowTitle(f"CodeCast - {file_name}")
                self.status_bar.showMessage(f"Файл {file_name} сохранен")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def search_text(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Поиск")
        dialog.setModal(True)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Поле для поиска
        search_layout = QtWidgets.QHBoxLayout()
        search_label = QtWidgets.QLabel("Найти:")
        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText("Введите текст для поиска...")
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)
        
        # Кнопки
        buttons_layout = QtWidgets.QHBoxLayout()
        
        find_button = QtWidgets.QPushButton("Найти")
        find_button.clicked.connect(lambda: self.find_text(search_input.text()))
        
        close_button = QtWidgets.QPushButton("Закрыть")
        close_button.clicked.connect(dialog.close)
        
        buttons_layout.addWidget(find_button)
        buttons_layout.addWidget(close_button)
        layout.addLayout(buttons_layout)
        
        dialog.exec()
    
    def find_text(self, text):
        if text:
            found = self.redactor_main_edit.find(text)
            if not found:
                # Если не найдено, начинаем с начала
                cursor = self.redactor_main_edit.textCursor()
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
                self.redactor_main_edit.setTextCursor(cursor)
                found = self.redactor_main_edit.find(text)
                if not found:
                    self.status_bar.showMessage(f"Текст '{text}' не найден")
    
    def run_code(self):
        # Получаем текущий код
        code = self.redactor_main_edit.toPlainText()
        
        # Создаем диалог для вывода
        output_dialog = QtWidgets.QDialog(self)
        output_dialog.setWindowTitle("Результат выполнения")
        output_dialog.setGeometry(200, 200, 600, 400)
        
        layout = QtWidgets.QVBoxLayout(output_dialog)
        
        output_text = QtWidgets.QTextEdit()
        output_text.setReadOnly(True)
        output_text.setFont(QtGui.QFont("Consolas", 10))
        layout.addWidget(output_text)
        
        close_button = QtWidgets.QPushButton("Закрыть")
        close_button.clicked.connect(output_dialog.close)
        layout.addWidget(close_button)
        
        # Перенаправляем stdout
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output
        
        try:
            exec(code)
            output = redirected_output.getvalue()
            if output:
                output_text.setPlainText(output)
            else:
                output_text.setPlainText("Код выполнен успешно (нет вывода)")
        except Exception as e:
            output_text.setPlainText(f"Ошибка выполнения:\n{str(e)}")
        finally:
            sys.stdout = old_stdout
        
        output_dialog.exec()
    
    def update_cursor_position(self):
        cursor = self.redactor_main_edit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.status_bar.showMessage(f"Строка: {line}, Колонка: {column}")
    
    def update_status(self):
        char_count = len(self.redactor_main_edit.toPlainText())
        line_count = self.redactor_main_edit.blockCount()
        self.setWindowTitle(f"CodeCast - {self.current_file if self.current_file else 'Новый файл'} ({line_count} строк, {char_count} символов)")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Устанавливаем стиль
    app.setStyle('Fusion')
    
    # Темная тема
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    
    app.setPalette(dark_palette)
    
    window = MainApplication()
    window.show()
    sys.exit(app.exec())