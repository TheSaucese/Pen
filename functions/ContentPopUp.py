from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QDialog, QVBoxLayout, QPushButton
from PySide6.QtGui import QScreen

class ContentPopup(QDialog):
    def __init__(self, file_content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Content")
        main_window_geometry = parent.geometry()
        screen_center = QScreen.availableGeometry(parent.screen()).center()

        self.setGeometry(
            screen_center.x() - main_window_geometry.width() / 2,
            screen_center.y() - main_window_geometry.height() / 2,
            main_window_geometry.width(),
            main_window_geometry.height()
        )
        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(file_content)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)