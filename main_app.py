import os
import json
from pathlib import Path
from PySide6 import QtWidgets, QtCore, QtGui

from widgets import TabWidget, CodeEditor, CodeFoldingArea, LineNumberArea, FileTreeDock, FindReplaceDialog, ThemeDialog
from utils import ThemeManager, ExtensionManager

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CodeCast Editor")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize managers
        self.theme_manager = ThemeManager()
        self.extension_manager = ExtensionManager()

        # Tab widget
        self.tab_widget = TabWidget(self.theme_manager, self.extension_manager, self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.new_tab()

        self.current_editor = None

        # File tree dock
        self.file_tree_dock = FileTreeDock(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.file_tree_dock)
        self.file_tree_dock.show()

        # Menus
        self.create_menus()

        # Status bar
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

        self.cursor_label = QtWidgets.QLabel("Line: 1, Col: 1")
        self.status_bar.addPermanentWidget(self.cursor_label)

        self.lines_label = QtWidgets.QLabel("Lines: 1")
        self.status_bar.addPermanentWidget(self.lines_label)

        # Autosave timer
        self.auto_save_timer = QtCore.QTimer()
        self.auto_save_timer.setInterval(30000)
        self.auto_save_timer.timeout.connect(self.auto_save_all)
        self.auto_save_timer.start()

        self.update_editor_connections()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Apply initial theme to whole app
        self.theme_manager.apply_theme_to_app(QtWidgets.QApplication.instance())

    def get_current_editor(self):
        return self.tab_widget.currentWidget()

    def update_editor_connections(self):
        editor = self.get_current_editor()
        if editor == self.current_editor:
            return
        if self.current_editor is not None:
            try:
                self.current_editor.cursorPositionChanged.disconnect()
            except (TypeError, RuntimeError):
                pass
            try:
                self.current_editor.blockCountChanged.disconnect()
            except (TypeError, RuntimeError):
                pass
            try:
                self.current_editor.textChanged.disconnect()
            except (TypeError, RuntimeError):
                pass
        if editor:
            editor.cursorPositionChanged.connect(self.update_cursor_position)
            editor.blockCountChanged.connect(self.update_line_count)
            editor.textChanged.connect(self.update_window_title)
        self.current_editor = editor

    def on_tab_changed(self, index):
        self.update_editor_connections()
        self.update_cursor_position()
        self.update_line_count()
        self.update_window_title()

    def update_cursor_position(self):
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            column = cursor.columnNumber() + 1
            self.cursor_label.setText(f"Line: {line}, Col: {column}")

    def update_line_count(self):
        editor = self.get_current_editor()
        if editor:
            lines = editor.blockCount()
            self.lines_label.setText(f"Lines: {lines}")

    def update_window_title(self):
        editor = self.get_current_editor()
        if editor:
            if editor.file_path:
                title = f"CodeCast - {os.path.basename(editor.file_path)}"
            else:
                title = "CodeCast - Untitled"
            if editor.is_modified:
                title = "*" + title
            self.setWindowTitle(title)

    def create_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        new_action = QtGui.QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QtGui.QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        open_root_action = QtGui.QAction("Open Folder as Root...", self)
        open_root_action.setShortcut("Ctrl+R")
        open_root_action.triggered.connect(self.choose_and_set_root)
        file_menu.addAction(open_root_action)

        file_menu.addSeparator()

        save_action = QtGui.QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_current_file)
        file_menu.addAction(save_action)

        save_as_action = QtGui.QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        save_all_action = QtGui.QAction("Save All", self)
        save_all_action.setShortcut("Ctrl+Alt+S")
        save_all_action.triggered.connect(self.save_all_files)
        file_menu.addAction(save_all_action)

        file_menu.addSeparator()

        close_tab_action = QtGui.QAction("Close Tab", self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(lambda: self.tab_widget.close_tab(self.tab_widget.currentIndex()))
        file_menu.addAction(close_tab_action)

        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        undo_action = QtGui.QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(lambda: self.get_current_editor().undo())
        edit_menu.addAction(undo_action)

        redo_action = QtGui.QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(lambda: self.get_current_editor().redo())
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QtGui.QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(lambda: self.get_current_editor().cut())
        edit_menu.addAction(cut_action)

        copy_action = QtGui.QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(lambda: self.get_current_editor().copy())
        edit_menu.addAction(copy_action)

        paste_action = QtGui.QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(lambda: self.get_current_editor().paste())
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        indent_action = QtGui.QAction("Increase Indent", self)
        indent_action.setShortcut("Tab")
        indent_action.triggered.connect(lambda: self.indent_selection())
        edit_menu.addAction(indent_action)

        unindent_action = QtGui.QAction("Decrease Indent", self)
        unindent_action.setShortcut("Shift+Tab")
        unindent_action.triggered.connect(lambda: self.unindent_selection())
        edit_menu.addAction(unindent_action)

        # Search menu
        search_menu = menubar.addMenu("Search")
        find_action = QtGui.QAction("Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.show_find_dialog)
        search_menu.addAction(find_action)

        replace_action = QtGui.QAction("Replace...", self)
        replace_action.setShortcut("Ctrl+H")
        replace_action.triggered.connect(self.show_replace_dialog)
        search_menu.addAction(replace_action)

        find_next_action = QtGui.QAction("Find Next", self)
        find_next_action.setShortcut("F3")
        find_next_action.triggered.connect(self.find_next)
        search_menu.addAction(find_next_action)

        find_prev_action = QtGui.QAction("Find Previous", self)
        find_prev_action.setShortcut("Shift+F3")
        find_prev_action.triggered.connect(self.find_previous)
        search_menu.addAction(find_prev_action)

        # View menu
        view_menu = menubar.addMenu("View")
        fold_all_action = QtGui.QAction("Fold All", self)
        fold_all_action.triggered.connect(self.fold_all)
        view_menu.addAction(fold_all_action)

        unfold_all_action = QtGui.QAction("Unfold All", self)
        unfold_all_action.triggered.connect(self.unfold_all)
        view_menu.addAction(unfold_all_action)

        view_menu.addSeparator()

        self.toggle_file_tree_action = QtGui.QAction("File Tree", self)
        self.toggle_file_tree_action.setCheckable(True)
        self.toggle_file_tree_action.setChecked(True)
        self.toggle_file_tree_action.triggered.connect(self.toggle_file_tree)
        self.toggle_file_tree_action.setShortcut("Ctrl+Shift+F")
        view_menu.addAction(self.toggle_file_tree_action)

        # Themes menu
        themes_menu = menubar.addMenu("Themes")
        choose_theme_action = QtGui.QAction("Choose Theme...", self)
        choose_theme_action.triggered.connect(self.show_theme_dialog)
        themes_menu.addAction(choose_theme_action)

    def new_file(self):
        self.tab_widget.new_tab()

    def open_file(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Open files", "", "All Files (*)")
        for file_path in file_paths:
            self.tab_widget.new_tab(file_path)

    def open_file_from_path(self, file_path):
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.file_path == file_path:
                self.tab_widget.setCurrentIndex(i)
                return
        self.tab_widget.new_tab(file_path)

    def choose_and_set_root(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Root Folder")
        if folder:
            self.file_tree_dock.set_root(folder)

    def save_current_file(self):
        editor = self.get_current_editor()
        if not editor:
            return False
        if editor.file_path:
            return editor.save_file(editor.file_path)
        else:
            return self.save_file_as()

    def save_file_as(self):
        editor = self.get_current_editor()
        if not editor:
            return False
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", "", "All Files (*)")
        if file_path:
            if not os.path.splitext(file_path)[1]:
                file_path += '.txt'
            if editor.save_file(file_path):
                editor.file_path = file_path
                editor.set_language_from_file(file_path)
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), os.path.basename(file_path))
                self.update_window_title()
                return True
        return False

    def save_all_files(self):
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.is_modified:
                if editor.file_path:
                    editor.save_file(editor.file_path)
                else:
                    self.tab_widget.setCurrentIndex(i)
                    self.save_file_as()

    def auto_save_all(self):
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.is_modified and editor.file_path:
                editor.save_file(editor.file_path)

    def show_find_dialog(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.show()

    def show_replace_dialog(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.replace_input.setEnabled(True)
        dialog.replace_btn.setEnabled(True)
        dialog.replace_all_btn.setEnabled(True)
        dialog.show()

    def find_next(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.find_next()

    def find_previous(self):
        dialog = FindReplaceDialog(self.get_current_editor(), self)
        dialog.find_previous()

    def indent_selection(self):
        editor = self.get_current_editor()
        if editor:
            editor.indent_selection()

    def unindent_selection(self):
        editor = self.get_current_editor()
        if editor:
            editor.unindent_selection()

    def fold_all(self):
        editor = self.get_current_editor()
        if editor:
            block = editor.document().begin()
            while block.isValid():
                if editor.is_foldable(block):
                    editor.toggle_fold(block)
                block = block.next()

    def unfold_all(self):
        editor = self.get_current_editor()
        if editor:
            editor.folded_blocks.clear()
            block = editor.document().begin()
            while block.isValid():
                block.setVisible(True)
                block = block.next()
            editor.folding_area.update()
            editor.line_number_area.update()

    def toggle_file_tree(self, checked=None):
        if checked is None:
            checked = self.toggle_file_tree_action.isChecked()
        if checked:
            self.file_tree_dock.show()
        else:
            self.file_tree_dock.hide()
        self.toggle_file_tree_action.setChecked(checked)

    def show_theme_dialog(self):
        dialog = ThemeDialog(self.theme_manager, self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            theme_name = dialog.get_selected_theme()
            if theme_name and self.theme_manager.set_theme(theme_name):
                # Apply theme to whole app
                self.theme_manager.apply_theme_to_app(QtWidgets.QApplication.instance())
                # Apply theme to all editors
                for i in range(self.tab_widget.count()):
                    editor = self.tab_widget.widget(i)
                    editor.apply_theme()
                # Force repaint of all widgets
                self.update()

    def run_code(self):
        editor = self.get_current_editor()
        if not editor:
            return
        code = editor.toPlainText()
        output_dialog = QtWidgets.QDialog(self)
        output_dialog.setWindowTitle("Execution Result")
        output_dialog.setGeometry(200, 200, 600, 400)
        layout = QtWidgets.QVBoxLayout(output_dialog)
        output_text = QtWidgets.QTextEdit()
        output_text.setReadOnly(True)
        output_text.setFont(QtGui.QFont("Consolas", 10))
        layout.addWidget(output_text)
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(output_dialog.close)
        layout.addWidget(close_button)

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
                output_text.setPlainText("Code executed successfully (no output)")
        except Exception as e:
            output_text.setPlainText(f"Execution error:\n{str(e)}")
        finally:
            sys.stdout = old_stdout
        output_dialog.exec()

    def closeEvent(self, event):
        unsaved = []
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.is_modified:
                unsaved.append(i)
        if unsaved:
            reply = QtWidgets.QMessageBox.question(
                self, "Unsaved changes",
                f"There are {len(unsaved)} files with unsaved changes. Save all?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.save_all_files()
                event.accept()
            elif reply == QtWidgets.QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()