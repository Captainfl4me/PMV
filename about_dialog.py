from PyQt6.QtWidgets import QWidget, QDialog, QLabel, QVBoxLayout

class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        
        self.setWindowTitle("About")
        self.setModal(True)
        
        app_title_label = QLabel("PMV - Post Mission Visualizer")
        author_name_label = QLabel("Author Name: Nicolas THIERRY")
        
        layout = QVBoxLayout()
        layout.addWidget(app_title_label)
        layout.addWidget(author_name_label)
        self.setLayout(layout)