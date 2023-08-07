from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTextBrowser, QGroupBox
from PySide6.QtCore import Signal,QThread,QObject,QUrl
from PySide6.QtGui import QTextCursor,QDesktopServices
from functions.scanner import crawl_website, open_ports,is_wordpress,scrape_urls


class ClickableTextBrowser(QTextBrowser):
    def __init__(self):
        super().__init__()

    def anchorClicked(self, url):
        # Open the clicked URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))


class ScanWorker(QObject):
    scan_progress = Signal(int)
    scan_results = Signal(str)

    def __init__(self):
        super().__init__()

    def start_scan(self, target_url):
        # Simulate scanning process for demonstration purposes
        open_ports_result, num = open_ports(target_url)
        is_wordpress_result = is_wordpress(target_url)
        crawled_urls = crawl_website(target_url, 20) # 20 max pages
        urls = scrape_urls(target_url)
        url_result = ""
        if urls:
            url_result += f"Scraped URLs:\n"
            for url in urls:
                url_result += f"{url}\n"
            for url in crawled_urls:
                url_result += f"{url}\n"
        else:
            url_result += "No URLs found or unable to retrieve information.\n"

        # Prepare the scan results step by step
        scan_results_parts = [
            f"{open_ports_result}\n",
            f"{is_wordpress_result}\n",
            f"{url_result}\n",
            f"Scanning complete! Found {num} open ports.\n",
            "Click for more details"
        ]

        # Send the scan results part by part
        for scan_result_part in scan_results_parts:
            self.scan_results.emit(scan_result_part)

class ScanWidget(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the main layout
        main_layout = QVBoxLayout(central_widget)

        # URL Input
        url_label = QLabel("Target URL:")
        self.url_input = QLineEdit("http://www.ngbsgroup.com")
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
        scan_results_label = QLabel("Scan Results:")
        self.scan_results = ClickableTextBrowser()
        main_layout.addWidget(scan_results_label)
        main_layout.addWidget(self.scan_results)

        # Scan History
        scan_history_group_box = QGroupBox("Scan History")
        scan_history_layout = QVBoxLayout()
        self.scan_history = QTextBrowser()
        self.scan_history.setReadOnly(True)
        scan_history_layout.addWidget(self.scan_history)
        scan_history_group_box.setLayout(scan_history_layout)
        main_layout.addWidget(scan_history_group_box)

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

        # Start the thread
        self.scan_thread.start()

        # Connect the Start Scan button to a function to start the scan process
        self.start_scan_button.clicked.connect(self.start_scan)

    def start_scan(self):
        target_url = self.url_input.text()

        self.scan_worker.start_scan(target_url)

    def update_scan_results(self, scan_result_part):
        # Append the received scan result part to the existing content of scan_results
        current_scan_results = self.scan_results.toPlainText() + scan_result_part + "\n"

        # Update the scan_results with the new content
        self.scan_results.setPlainText(current_scan_results)

        # Move the cursor to the end of the QTextBrowser to see the latest updates
        text_cursor = self.scan_results.textCursor()
        text_cursor.movePosition(QTextCursor.End)
        self.scan_results.setTextCursor(text_cursor)

    def update_scan_progress(self, progress_value):
        # Update the scan_progress bar with the received value
        self.scan_progress.setValue(progress_value)
    
    def closeEvent(self, event):
        # Clean up the thread and worker when the GUI is closed
        self.scan_thread.quit()
        self.scan_thread.wait()
        super().closeEvent(event)

    
    