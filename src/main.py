import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QFileDialog, QListWidget, 
    QLabel, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt
from pathlib import Path
from core.data_loader import DataLoader
from ui.main_window import ReviewWindow

class PikFixApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PikFix - AI Training Data Review Tool")
        self.resize(600, 400)
        
        self.data_loader = DataLoader()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 1. Root Path Selection
        root_layout = QHBoxLayout()
        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Select root data directory...")
        self.root_edit.textChanged.connect(self.on_root_changed)
        
        self.btn_browse_root = QPushButton("Browse")
        self.btn_browse_root.clicked.connect(self.browse_root)
        
        root_layout.addWidget(QLabel("Root Path:"))
        root_layout.addWidget(self.root_edit)
        root_layout.addWidget(self.btn_browse_root)
        layout.addLayout(root_layout)

        # 2. Folder Selection
        folders_layout = QHBoxLayout()
        
        # Source Folder Selection
        source_vbox = QVBoxLayout()
        source_vbox.addWidget(QLabel("Source Folder (1):"))
        self.source_list = QListWidget()
        self.source_list.setSelectionMode(QAbstractItemView.SingleSelection)
        source_vbox.addWidget(self.source_list)
        
        # Candidate Folders Selection
        candidate_vbox = QVBoxLayout()
        candidate_vbox.addWidget(QLabel("Candidate Folders (N):"))
        self.candidate_list = QListWidget()
        self.candidate_list.setSelectionMode(QAbstractItemView.MultiSelection)
        candidate_vbox.addWidget(self.candidate_list)
        
        folders_layout.addLayout(source_vbox)
        folders_layout.addLayout(candidate_vbox)
        layout.addLayout(folders_layout)

        # 3. Action Button
        self.btn_start = QPushButton("Load Images and Start Review")
        self.btn_start.clicked.connect(self.start_review)
        self.btn_start.setEnabled(False)
        layout.addWidget(self.btn_start)

    def browse_root(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Root Directory")
        if directory:
            self.root_edit.setText(directory)

    def on_root_changed(self, text):
        self.data_loader.root_path = Path(text) if text else Path("")
        self.refresh_folders()

    def refresh_folders(self):
        # Clear current lists
        self.source_list.clear()
        self.candidate_list.clear()
        
        folders = self.data_loader.get_subfolders()
        self.source_list.addItems(folders)
        self.candidate_list.addItems(folders)
        
        # Link source selection to candidate list filtering
        self.source_list.currentItemChanged.connect(self.filter_candidates)
        
        self.btn_start.setEnabled(len(folders) > 0)

    def filter_candidates(self, current, previous):
        if current:
            source_folder = current.text()
            # Automatically select all folders except the source folder
            for i in range(self.candidate_list.count()):
                item = self.candidate_list.item(i)
                if item.text() != source_folder:
                    item.setSelected(True)
                else:
                    item.setSelected(False)

    def start_review(self):
        source_item = self.source_list.currentItem()
        selected_candidates = self.candidate_list.selectedItems()
        
        if not source_item:
            QMessageBox.warning(self, "Warning", "Please select a source folder.")
            return
        
        if not selected_candidates:
            QMessageBox.warning(self, "Warning", "Please select at least one candidate folder.")
            return
            
        source_folder = source_item.text()
        candidate_folders = [item.text() for item in selected_candidates]
        
        # For now, using root_path as output_path. 
        # I will add a dedicated output path selector in the next turn.
        output_folder = self.data_loader.root_path 
        
        try:
            matched_data = self.data_loader.match_images(source_folder, candidate_folders)
            
            if not matched_data:
                QMessageBox.warning(self, "Warning", "No matching images found between selected folders.")
                return

            # SESSION MANAGEMENT: Check for existing progress
            from core.storage import ProgressManager
            progress_mgr = ProgressManager(str(self.data_loader.root_path))
            saved_data = progress_mgr.load_progress()
            
            if saved_data.get("current_index", 0) > 0:
                reply = QMessageBox.question(
                    self, "Resume Session", 
                    f"Previous progress found. Resume from image {saved_data['current_index'] + 1}?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    progress_mgr.clear_progress()
                    saved_data = {"current_index": 0, "selections": {}}

            # Transition to the Review Window with output_folder
            self.review_window = ReviewWindow(matched_data, str(self.data_loader.root_path), str(output_folder))
            self.review_window.show()
            self.hide() 
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while matching images:\n{str(e)}")

if __name__ == "__main__":
    from pathlib import Path # Added here because it's used in on_root_changed
    app = QApplication(sys.argv)
    window = PikFixApp()
    window.show()
    sys.exit(app.exec())
