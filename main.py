"""
PMV - Post Mission Visualizer
Author: Nicolas THIERRY
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar
from PyQt6.QtGui import QAction

from folder_selector import FolderSelector
from about_dialog import AboutDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PMV - Post Mission Visualizer")
        
        # Create the menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
         
        file_menu = menu_bar.addMenu("&File")
        import_action = QAction("Import", self)
        import_action.triggered.connect(self.show_folder_selector)
        file_menu.addAction(import_action)
        
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        layout = QVBoxLayout()
        
        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_folder_selector(self):
        self.folder_selector = FolderSelector()
        self.folder_selector.show()

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    