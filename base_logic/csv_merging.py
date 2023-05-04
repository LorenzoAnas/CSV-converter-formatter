import os
import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QFileDialog
from PyQt6 import QtCore

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

        # Connect the drop label to the on_drop method
        self.drop_label.setAcceptDrops(True)
        self.drop_label.dragEnterEvent = self.drag_enter_event
        self.drop_label.dropEvent = self.drop_event

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        # Get the file paths from the dropped URLs
        file_paths = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.csv'):
                file_paths.append(file_path)

        # Merge the CSV files and save the result
        if file_paths:
            merged_csv = self.merge_csv_files(file_paths)
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Save merged CSV file", "", "CSV files (*.csv)")
            if file_path:
                with open(file_path, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for row in merged_csv:
                        writer.writerow(row)

    def merge_csv_files(self, file_paths):
        # Merge the CSV files
        merged_csv = []
        for file_path in file_paths:
            with open(file_path, newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    merged_csv.append(row)

        return merged_csv

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MergeCSV()
    window.show()
    sys.exit(app.exec())
