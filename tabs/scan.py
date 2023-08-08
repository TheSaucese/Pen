from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTextBrowser, QGroupBox,QHBoxLayout,QSizePolicy,QTableWidgetItem,QTableWidget,QHeaderView,QAbstractItemView
from PySide6.QtCore import Signal,QThread,QObject,QUrl,QSize,Qt
from PySide6.QtGui import QTextCursor,QDesktopServices
from functions.ScanOptionsDialog import ScanOptionsDialog
from functions.ScanSaveOption import ScanSaveOptionsDialog
from functions.scanner import crawl_website, open_ports,is_wordpress,scrape_urls
from datetime import datetime
import os

class ClickableTextBrowser(QTextBrowser):
    saveRequested = Signal()

    def __init__(self):
        super().__init__()
        self.save_scan_button = QPushButton("Save", self)
        self.save_scan_button.setFixedSize(QSize(45,40))
        self.save_scan_button.clicked.connect(self.emit_save_signal)

    def anchorClicked(self, url):
        # Open the clicked URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))

    def resizeEvent(self, event):
        self.save_scan_button.move(self.width() - self.save_scan_button.width(), 1)
        super().resizeEvent(event)

    def emit_save_signal(self):
        self.saveRequested.emit()  # Emit a custom signal when the button is clicked

    def enable_save_button(self):
        self.save_scan_button.setEnabled(True)  # Enable the button

    def disable_save_button(self):
        self.save_scan_button.setEnabled(False)  # Disable the button
    

    


class ScanWorker(QObject):
    scan_progress = Signal(int)
    scan_results = Signal(str)

    def __init__(self):
        super().__init__()

    def start_scan(self, target_url,selected_options):
        # Simulate scanning process for demonstration purposes
        open_ports_result=""
        num=""
        is_wordpress_result=""
        url_result=""
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

class ScanWidget(QWidget):

    DEFAULT_SAVE_DIR = "saves"  # Default directory for saving scan results

    def __init__(self):
        super().__init__()
        # Create the default save directory if it doesn't exist
        if not os.path.exists(self.DEFAULT_SAVE_DIR):
            os.makedirs(self.DEFAULT_SAVE_DIR)

        # Populate saved_scan_results with files from the saves directory
        self.saved_scan_results = self.load_saved_scan_results()

        self.options= ScanOptionsDialog(self).get_selected_options()

        
        # Create the main layout
        main_layout = QVBoxLayout(self)

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
        scan_results_group_box = QGroupBox("Scan Results:")
        scan_results_layout = QVBoxLayout()
        self.scan_results = ClickableTextBrowser()
        self.scan_results.setReadOnly(True)
        scan_results_layout.addWidget(self.scan_results)
        scan_results_group_box.setLayout(scan_results_layout)
        main_layout.addWidget(scan_results_group_box)

        self.scan_results.saveRequested.connect(self.save_scan_results)
    

        # Scan History
        scan_history_group_box = QGroupBox("Scan History")
        scan_history_layout = QVBoxLayout()
        self.scan_results_table = QTableWidget()
        self.scan_results_table.setColumnCount(1)  # One column for scan results
        self.scan_results_table.setHorizontalHeaderLabels(["Saved Scans"])
        self.scan_results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.scan_results_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        scan_history_layout.addWidget(self.scan_results_table)
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
        self.scan_options_button.clicked.connect(self.open_scan_options)
        #self.save_scan_button.clicked.connect(self.save_scan_results)

        self.scan_results.disable_save_button()

        # Start the thread
        self.scan_thread.start()

        # Connect the Start Scan button to a function to start the scan process
        self.start_scan_button.clicked.connect(self.start_scan)

        self.update_scan_history()

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
        self.scan_results.clear()
        self.scan_worker.start_scan(target_url,self.options)
        self.scan_results.enable_save_button()

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

    def get_file_date(self,file_name):
        # Extract the date and time portion from the filename
        date_str = file_name.split('_')[1]  # Splitting by '_' and getting the second part
        time_str = file_name.split('_')[2]  # Splitting by '_' and getting the third part

        # Combine the date and time strings to create a datetime object
        datetime_str = f"{date_str}_{time_str}"
        file_datetime = datetime.strptime(datetime_str, "%Y-%m-%d_%H-%M-%S")

        return file_datetime.date()

    def save_scan_results(self):
        scan_results = self.scan_results.toPlainText()

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
            self.update_scan_history()
        except Exception as e:
            print("Error saving scan results:", e)

        self.scan_results.disable_save_button()
        

    def update_scan_history(self):
        self.scan_results_table.setRowCount(0)  # Clear the existing rows

        for _,scan_date in enumerate(self.saved_scan_results, start=1):
            self.scan_results_table.insertRow(0)  # Insert a new row at the top

            date_item = QTableWidgetItem(scan_date)
            self.scan_results_table.setItem(0, 0, date_item)

    def display_scan_result(self, item):
        row = item.row()
        if 0 <= row < len(self.saved_scan_results):
            scan_result = self.saved_scan_results[row]
            self.scan_results.setPlainText(scan_result)
            # Additional logic if needed, such as scrolling to the top
