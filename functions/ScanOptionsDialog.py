from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox,QLabel
from PySide6.QtCore import Qt

class ScanOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scan Options")
        self.setFixedSize(250, 150)
       

        layout = QVBoxLayout(self)
        self.checkboxes = []

        # Create checkboxes for different scan options and set their initial states
        self.port_scan_checkbox = QCheckBox("Open Ports Scan")
        self.port_scan_checkbox.setChecked(True)  # Ticked by default
        self.wordpress_scan_checkbox = QCheckBox("WordPress Detection")
        self.wordpress_scan_checkbox.setChecked(True)  # Ticked by default
        self.url_scan_checkbox = QCheckBox("URL Scraping")
        self.url_scan_checkbox.setChecked(True)  # Ticked by default

        layout.addWidget(self.port_scan_checkbox)
        layout.addWidget(self.wordpress_scan_checkbox)
        layout.addWidget(self.url_scan_checkbox)

        self.message_label = QLabel("You must select at least one option.")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: red;")
        self.message_label.hide()
        layout.addWidget(self.message_label)    

        # Add dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def validate_and_accept(self):
        selected_options = self.get_selected_options()
        if selected_options:
            self.accept()
        else:
            self.message_label.show()

    def get_selected_options(self):
        selected_options = []
        if self.port_scan_checkbox.isChecked():
            selected_options.append("Open Ports Scan")
        if self.wordpress_scan_checkbox.isChecked():
            selected_options.append("WordPress Detection")
        if self.url_scan_checkbox.isChecked():
            selected_options.append("URL Scraping")
        return selected_options
