import sys
from PySide6 import QtWidgets
from main_app import MainApplication

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    # Применяем тёмную палитру по умолчанию, но она будет перезаписана текущей темой
    window = MainApplication()
    window.show()
    sys.exit(app.exec())