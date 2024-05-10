import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem,QSizePolicy,QHeaderView,QLabel,QCheckBox,QDialog

class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Options Window")
        self.setMinimumWidth(200)

        main_layout = QVBoxLayout(self)

        # Add checkable items (you can add more as needed)
        option1_checkbox = QCheckBox("Option 1")
        option2_checkbox = QCheckBox("Option 2")
        option3_checkbox = QCheckBox("Option 3")

        main_layout.addWidget(option1_checkbox)
        main_layout.addWidget(option2_checkbox)
        main_layout.addWidget(option3_checkbox)

class VulnWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Top Box
        top_box = QWidget(self)
        main_layout.addWidget(top_box)

        top_box_layout = QHBoxLayout()
        top_box.setLayout(top_box_layout)

        # First Horizontal Box in Top Section
        first_horizontal_box = QWidget(self)
        top_box_layout.addWidget(first_horizontal_box)

        first_horizontal_layout = QVBoxLayout()
        first_horizontal_box.setLayout(first_horizontal_layout)

        start_button = QPushButton("Start", self)
        options_button = QPushButton("Options", self)
        options_button.clicked.connect(self.open_options_window)  # Connect the button click to open_options_window
        first_horizontal_layout.addWidget(start_button)
        first_horizontal_layout.addWidget(options_button)

        # Second Horizontal Box in Top Section
        second_horizontal_box = QWidget(self)
        top_box_layout.addWidget(second_horizontal_box)

        second_horizontal_layout = QVBoxLayout()
        second_horizontal_box.setLayout(second_horizontal_layout)

        status_label = QLabel("Total Vulnerabilities", self)
        progress_bar = QProgressBar(self)
        progress_bar.setValue(50)  # You can set the progress value as needed
        estimated_time_label = QLabel("Estimated Time: 1h 30m", self)

        second_horizontal_layout.addWidget(status_label)
        second_horizontal_layout.addWidget(progress_bar)
        second_horizontal_layout.addWidget(estimated_time_label)

        # Bottom Box
        bottom_box = QWidget(self)
        main_layout.addWidget(bottom_box)

        bottom_box_layout = QVBoxLayout(bottom_box)  # Set the parent to bottom_box
        bottom_box.setLayout(bottom_box_layout)

        # Create and populate the table
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Name", "Date", "CVE Score"])
        header = table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # Example data (you can add your own data here)
        data = [
            ("Vulnerability 1", "2023-07-31", "7.5"),
            ("Vulnerability 2", "2023-07-30", "8.0"),
            ("Vulnerability 3", "2023-07-29", "9.5"),
        ]

        for row, (name, date, score) in enumerate(data):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(date))
            table.setItem(row, 2, QTableWidgetItem(score))

        bottom_box_layout.addWidget(table)

        # Make the top_box fixed size and stretch the bottom_box
        top_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        bottom_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def open_options_window(self):
        options_window = OptionsWindow()
        options_window.exec()


