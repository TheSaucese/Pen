from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox,QFileDialog,QLineEdit,QPushButton

class ScanSaveOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Scan Results")

        layout = QVBoxLayout(self)

        self.file_path_edit = QLineEdit()
        layout.addWidget(self.file_path_edit)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_for_file)
        layout.addWidget(self.browse_button)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def browse_for_file(self):
        file_dialog = QFileDialog(self, "Save Scan Results", "", "Text Files (*.txt)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            self.file_path_edit.setText(selected_file)

    def get_selected_file_path(self):
        return self.file_path_edit.text() if self.file_path_edit.text() else None
