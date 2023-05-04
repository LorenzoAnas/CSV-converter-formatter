import os
import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QFileDialog, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6 import QtCore, Qt, QtGui






class MergeCSV(QMainWindow):
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
        self.drop_label.setFixedSize(200, 100)
        self.drop_label.setStyleSheet("background-color: lightgray")
        self.drop_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.drop_label, 0, 0, 1, 2)

        # Create a button for merging the files
        self.merge_button = QPushButton("Merge Files")
        self.merge_button.setDisabled(True)
        layout.addWidget(self.merge_button, 1, 0, 1, 2)

        # Connect the drop label to the on_drop method
        self.file_paths = []
        self.drop_label.setAcceptDrops(True)
        self.drop_label.dragEnterEvent = self.drag_enter_event
        self.drop_label.dropEvent = self.drop_event
        self.merge_button.clicked.connect(self.merge_files)

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

            # call check_csv_file method to update the status of the file
            self.check_csv_file(file_path)
    
        # Enable the merge button if there are files to merge
        if self.file_paths:
            self.merge_button.setDisabled(False)

        # Add the file paths to the table
        for i, file_path in enumerate(self.file_paths):
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            # Add index number
            index_item = QTableWidgetItem(str(i))
            index_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setItem(row_position, 0, index_item)

            # Add file path
            path_item = QTableWidgetItem(file_path)
            path_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            self.table_widget.setItem(row_position, 1, path_item)

            # Add status
            status_item = QTableWidgetItem()
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if self.check_csv_file(file_path):
                status_item.setIcon(QtGui.QIcon('check.png'))
            else:
                status_item.setIcon(QtGui.QIcon('cross.png'))
            self.table_widget.setItem(row_position, 2, status_item)

        # Enable the merge button if there are files to merge
        if self.file_paths:
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

            # Show a message indicating the merge was successful
            msg_box = QMessageBox()
            msg_box.setText("CSV files merged successfully!")
            msg_box.exec()

    def merge_csv_files(self, file_paths):
        # Merge the CSV files
        merged_csv = []
        for file_path in file_paths:
            with open(file_path, newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    merged_csv.append(row)

        return merged_csv
    
    def check_csv_file(self, file_path):
        try:
            with open(file_path, newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    pass
        except Exception as e:
            return False

        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MergeCSV()
    window.show()
    sys.exit(app.exec())
