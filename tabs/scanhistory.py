# Scan History
scan_history_group_box = QGroupBox("Scan History")
scan_history_layout = QVBoxLayout()
self.scan_results_table = QTableWidget()
self.scan_results_table.setColumnCount(1)  # One column for scan results
self.scan_results_table.setHorizontalHeaderLabels(["Saved Scans"])
self.scan_results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
self.scan_results_table.cellDoubleClicked.connect(self.handle_cell_double_clicked)
header = self.scan_results_table.horizontalHeader()
header.setSectionResizeMode(0, QHeaderView.Stretch)

scan_history_layout.addWidget(self.scan_results_table)
scan_history_group_box.setLayout(scan_history_layout)
main_layout.addWidget(scan_history_group_box)

def update_scan_history(self):
        self.scan_results_table.setRowCount(0)  # Clear the existing rows

        for _, scan_date in enumerate(self.saved_scan_results, start=1):
            self.scan_results_table.insertRow(0)  # Insert a new row at the top

            date_item = QTableWidgetItem(scan_date)
            self.scan_results_table.setItem(0, 0, date_item)


def handle_cell_double_clicked(self, row, col):
        file_name_item = self.scan_results_table.item(row, col)
        if file_name_item is not None:
            file_name = file_name_item.text()
            try:
                with open("saves/" + file_name, "r") as file:
                    file_content = file.read()
                    popup = ContentPopup(file_content, parent=self)
                    popup.exec_()
            except FileNotFoundError:
                print("File not found.")
        else:
            print("No item at the clicked cell.")

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