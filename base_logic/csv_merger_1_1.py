import os
import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QFileDialog, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt6 import QtCore

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the main window
        self.setWindowTitle("CSV Merger")
        self.setGeometry(100, 100, 600, 400)
    
        # Create a central widget to hold the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QGridLayout()
        central_widget.setLayout(layout)
        
        # Create a label for the drop area
        self.drop_label = QLabel("Drop CSV files here")
        self.drop_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.drop_label.setStyleSheet("background-color: lightgray")
        self.drop_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.drop_label, 0, 0, 1, 2)
    
        # Create a table for displaying the CSV file 
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(['File Name'])
        layout.addWidget(self.table_widget, 1, 0, 1, 1)

        # Create a button for merging the files
        self.merge_button = QPushButton("Merge Files")
        self.merge_button.setDisabled(True)
        layout.addWidget(self.merge_button, 3, 0, 1, 2)

        # Create browse button
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse)
        layout.addWidget(self.browse_button, 2, 0, 1, 2)

        # Connect the drop label to the on_drop method
        self.file_paths = []
        self.drop_label.setAcceptDrops(True)
        self.drop_label.dragEnterEvent = self.drag_enter_event
        self.drop_label.dropEvent = self.drop_event
        self.merge_button.clicked.connect(self.merge_files)

    def browse(self):
        # Start the file dialog from the desktop folder
        starting_folder = os.path.expanduser("~/Desktop")
        file_dialog = QFileDialog(self, "Select a file", starting_folder, "CSV files (*.csv)")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.file_paths.append(file_path)
            self.add_csv_file_to_table(file_path=file_path)
            self.merge_button.setDisabled(False)
        else:
            return None

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        # Get the file paths from the dropped URLs
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.csv'):
                self.file_paths.append(file_path)
                self.add_csv_file_to_table(file_path=file_path)
                self.merge_button.setDisabled(False)

    def merge_files(self):
        # Merge the CSV files and save the result
        if self.file_paths:
            merged_csv = self.merge_csv_files(self.file_paths)
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Save merged CSV file", "", "CSV files (*.csv)")
            if file_path:
                with open(file_path, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for row in merged_csv:
                        writer.writerow(row)

            # Clear the file paths and disable the merge button
            self.file_paths = []
            self.merge_button.setDisabled(True)

    def merge_csv_files(self, file_paths):
        # Merge the CSV files
        merged_csv = []
        for file_path in file_paths:
            with open(file_path, newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    merged_csv.append(row)

        return merged_csv
    
    def add_csv_file_to_table(self, file_path):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        file_name = QTableWidgetItem(file_path.split("/")[-1])
        file_name.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.table_widget.setItem(row_position, 0, file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
