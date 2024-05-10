from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTextBrowser, QGroupBox, QHBoxLayout, QSizePolicy, QTableWidgetItem, QTableWidget, QHeaderView, QAbstractItemView, QTextEdit, QGridLayout
from PySide6.QtCore import Signal, QThread, QObject, QUrl, QSize
from PySide6.QtGui import QTextCursor, QDesktopServices
from functions.ContentPopUp import ContentPopup
from functions.ScanOptionsDialog import ScanOptionsDialog
from functions.ScanSaveOption import ScanSaveOptionsDialog
from functions.scanner import WappAlyze, crawl_website, open_ports, is_wordpress, scrape_urls
from functions.xsstrike import run_xsstrike
from functions.dirbuster import run_feroxbuster
from datetime import datetime
import os

class ClickableTextBrowser(QTextBrowser):
    saveRequested = Signal()

    def __init__(self):
        super().__init__()
        self.save_button = QPushButton("Save", self)
        self.save_button.setFixedSize(QSize(45, 40))
        self.save_button.clicked.connect(self.emit_save_signal)

    def anchorClicked(self, url):
        # Open the clicked URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))

    def resizeEvent(self, event):
        self.save_button.move(self.width() - self.save_button.width(), 1)
        super().resizeEvent(event)

    def emit_save_signal(self):
        self.saveRequested.emit()  # Emit a custom signal when the button is clicked

    def enable_save_button(self):
        self.save_button.setEnabled(True)  # Enable the button

    def disable_save_button(self):
        self.save_button.setEnabled(False)  # Disable the button

class ScanResultWidget(QWidget):
    def __init__(self, title, content):
        super().__init__()
        layout = QVBoxLayout(self)
        self.title_label = QLabel(title)
        layout.addWidget(self.title_label)
        self.content_text_edit = QTextEdit()
        self.content_text_edit.setPlainText(content)
        self.content_text_edit.setReadOnly(True)
        layout.addWidget(self.content_text_edit)
        self.setVisible(False)

class ScanWorker(QObject):
    scan_progress = Signal(int)
    scan_results = Signal(str)

    def __init__(self):
        super().__init__()

    def start_scan(self, target_url, selected_options):
        # Simulate scanning process for demonstration purposes
        open_ports_result = ""
        num = ""
        is_wordpress_result = ""
        url_result = ""
        wap = WappAlyze(target_url)
        wap_result = ""
        xsstrike_result = run_xsstrike(target_url)
        dirbuster_result = run_feroxbuster(target_url)
        if "Open Ports Scan" in selected_options:
            open_ports_result, num = open_ports(target_url)

        if "WordPress Detection" in selected_options:
            is_wordpress_result = is_wordpress(target_url)

        if "URL Scraping" in selected_options:
            urls = scrape_urls(target_url)
            curls = crawl_website(target_url)
            url_result = ""
            if urls:
                url_result += f"Scraped URLs:\n"
                for url in urls:
                    url_result += f"{url}\n"
                for url in curls:
                    url_result += f"{url}\n"
            else:
                url_result += "No URLs found or unable to retrieve information.\n"

            for w in wap:
                wap_result += f"{w}\n"

        # Prepare the scan results step by step
        scan_results_parts = [
            ("Open Ports Scan", open_ports_result),
            ("WordPress Detection", is_wordpress_result),
            ("URL Scraping", url_result),
            ("WappAlyze", wap_result),
            ("XSStrike", xsstrike_result),
            ("DirBuster", dirbuster_result)
        ]

        # Send the scan results part by part
        for title, content in scan_results_parts:
            self.scan_results.emit(f"{title}\n{content}\n")

class ScanWidget(QWidget):

    DEFAULT_SAVE_DIR = "saves"  # Default directory for saving scan results

    def __init__(self):
        super().__init__()
        # Create the default save directory if it doesn't exist
        if not os.path.exists(self.DEFAULT_SAVE_DIR):
            os.makedirs(self.DEFAULT_SAVE_DIR)

        # Populate saved_scan_results with files from the saves directory
        self.saved_scan_results = self.load_saved_scan_results()

        self.options = ScanOptionsDialog(self).get_selected_options()

        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Information Gathering")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # URL Input
        url_label = QLabel("Target URL:")
        self.url_input = QLineEdit()
        main_layout.addWidget(url_label)
        main_layout.addWidget(self.url_input)

        # Start Scan Button
        self.start_scan_button = QPushButton("Start Scan")
        main_layout.addWidget(self.start_scan_button)

        # Scan Options Button
        self.scan_options_button = QPushButton("Scan Options")
        main_layout.addWidget(self.scan_options_button)

        # Scan Progress
        self.scan_progress = QProgressBar()
        main_layout.addWidget(self.scan_progress)

        # Scan Results
        scan_results_group_box = QGroupBox("Scan Results:")
        scan_results_layout = QGridLayout()
        self.scan_results_widgets = []
        for i in range(3):  # Assuming there are 9 scan result parts
            for j in range(3):
                scan_result_widget = ScanResultWidget("", "")
                scan_results_layout.addWidget(scan_result_widget, i, j)
                self.scan_results_widgets.append(scan_result_widget)
        scan_results_group_box.setLayout(scan_results_layout)
        main_layout.addWidget(scan_results_group_box)

        # Save Button
        self.save_button = QPushButton("Save All")
        main_layout.addWidget(self.save_button)

        # Help/About
        help_about_group_box = QGroupBox("Help/About")
        help_about_layout = QVBoxLayout()
        help_about_layout.addWidget(QLabel("Version: 1.0"))
        help_about_layout.addWidget(QLabel("Documentation"))
        help_about_group_box.setLayout(help_about_layout)
        main_layout.addWidget(help_about_group_box)

        # Create a worker object and a separate thread for the scanning process
        self.scan_thread = QThread()
        self.scan_worker = ScanWorker()
        self.scan_worker.moveToThread(self.scan_thread)

        # Connect the worker signals to the GUI slots
        self.scan_worker.scan_results.connect(self.update_scan_results)
        self.scan_worker.scan_progress.connect(self.update_scan_progress)
        self.scan_options_button.clicked.connect(self.open_scan_options)

        # Connect save button signal
        self.save_button.clicked.connect(self.save_scan_results)

        # Start the thread
        self.scan_thread.start()

        # Connect the Start Scan button to a function to start the scan process
        self.start_scan_button.clicked.connect(self.start_scan)

    def load_saved_scan_results(self):
        saved_scan_results = []
        for file_name in os.listdir(self.DEFAULT_SAVE_DIR):
            saved_scan_results.append(file_name)
        return saved_scan_results

    def open_scan_options(self):
        options_dialog = ScanOptionsDialog(self)
        if options_dialog.exec_():
            # Dialog was accepted, handle the selected options here
            self.options = options_dialog.get_selected_options()

    def start_scan(self):
        target_url = self.url_input.text()
        for widget in self.scan_results_widgets:
            widget.hide()
        self.scan_worker.start_scan(target_url, self.options)

    def update_scan_results(self, scan_result_part):
        for i, widget in enumerate(self.scan_results_widgets):
            if not widget.isVisible():
                title, content = scan_result_part.split('\n', 1)
                widget.title_label.setText(title)
                widget.content_text_edit.setPlainText(content)
                widget.show()
                break

    def update_scan_progress(self, progress_value):
        # Update the scan_progress bar with the received value
        self.scan_progress.setValue(progress_value + self.scan_progress.value)

    def closeEvent(self, event):
        # Clean up the thread and worker when the GUI is closed
        self.scan_thread.quit()
        self.scan_thread.wait()
        super().closeEvent(event)

    def get_file_date(self, file_name):
        # Extract the date and time portion from the filename
        date_str = file_name.split('_')[1]  # Splitting by '_' and getting the second part
        time_str = file_name.split('_')[2]  # Splitting by '_' and getting the third part

        # Combine the date and time strings to create a datetime object
        datetime_str = f"{date_str}_{time_str}"
        file_datetime = datetime.strptime(datetime_str, "%Y-%m-%d_%H-%M-%S")

        return file_datetime.date()

    def save_scan_results(self):
        # Save all scan results to a single file
        scan_results = ""
        for widget in self.scan_results_widgets:
            title = widget.title_label.text()
            content = widget.content_text_edit.toPlainText()
            scan_results += f"{title}\n{content}\n\n"

        # Construct the file path for saving the scan results
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"scan_{current_time}.txt"
        file_path = os.path.join(self.DEFAULT_SAVE_DIR, file_name)

        try:
            with open(file_path, "w") as file:
                file.write(scan_results)
            print(f"Scan results saved in {file_path}")

            # Add the saved scan results to the history
            self.saved_scan_results.append(file_name)

            # Update the scan history widget
            # self.update_scan_history()
        except Exception as e:
            print("Error saving scan results:", e)