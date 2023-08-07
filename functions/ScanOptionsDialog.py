from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox

class ScanOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scan Options")

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

        # Add dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_selected_options(self):
        selected_options = []
        if self.port_scan_checkbox.isChecked():
            selected_options.append("Open Ports Scan")
        if self.wordpress_scan_checkbox.isChecked():
            selected_options.append("WordPress Detection")
        if self.url_scan_checkbox.isChecked():
            selected_options.append("URL Scraping")
        return selected_options
