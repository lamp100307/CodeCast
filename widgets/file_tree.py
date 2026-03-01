from PySide6 import QtWidgets, QtCore
import os

class FileTreeDock(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super().__init__("File Tree", parent)
        self.parent = parent
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        self.tree_view = QtWidgets.QTreeView()
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
        self.tree_view.setModel(self.model)
        self.set_root_to_current_dir()

        # Hide size, type, date columns
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        self.tree_view.doubleClicked.connect(self.on_file_double_clicked)
        self.tree_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

        self.setWidget(self.tree_view)

    def set_root_to_current_dir(self):
        current_dir = QtCore.QDir.currentPath()
        self.tree_view.setRootIndex(self.model.index(current_dir))

    def set_root(self, path):
        if os.path.isdir(path):
            self.tree_view.setRootIndex(self.model.index(path))

    def on_file_double_clicked(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.parent.open_file_from_path(path)

    def show_context_menu(self, position):
        index = self.tree_view.indexAt(position)
        if not index.isValid():
            return
        path = self.model.filePath(index)
        menu = QtWidgets.QMenu()
        if os.path.isdir(path):
            open_folder_action = menu.addAction("Open as Root")
            open_folder_action.triggered.connect(lambda: self.set_root(path))
        menu.exec(self.tree_view.viewport().mapToGlobal(position))