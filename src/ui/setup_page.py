import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QListWidget, 
    QLabel, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt
from pathlib import Path

class SetupPage(QWidget):
    """
    The initial configuration page where the user selects the root directory 
    and defines the source/candidate folders.
    """
    def __init__(self, data_loader, on_start_callback):
        super().__init__()
        self.data_loader = data_loader
        self.on_start_callback = on_start_callback
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Header
        header = QLabel("Welcome to PikFix")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)

        # 1. Root Path Selection
        root_box = QVBoxLayout()
        root_label = QLabel("<b>Step 1: Select Root Data Directory</b>")
        root_label.setAlignment(Qt.AlignCenter)
        
        root_layout = QHBoxLayout()
        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Select path to your image datasets...")
        self.root_edit.textChanged.connect(self.on_root_changed)
        
        self.btn_browse_root = QPushButton("Browse")
        self.btn_browse_root.clicked.connect(self.browse_root)
        
        root_layout.addWidget(self.root_edit)
        root_layout.addWidget(self.btn_browse_root)
        
        root_box.addWidget(root_label)
        root_box.addLayout(root_layout)
        layout.addLayout(root_box)

        # 2. Folder Selection
        folders_box = QVBoxLayout()
        folders_label = QLabel("<b>Step 2: Configure Folders</b>")
        folders_label.setAlignment(Qt.AlignCenter)
        
        folders_layout = QHBoxLayout()
        
        # Source Folder
        source_vbox = QVBoxLayout()
        source_vbox.addWidget(QLabel("Source Folder (1):"))
        self.source_list = QListWidget()
        self.source_list.setSelectionMode(QAbstractItemView.SingleSelection)
        source_vbox.addWidget(self.source_list)
        
        # Candidate Folders
        candidate_vbox = QVBoxLayout()
        candidate_vbox.addWidget(QLabel("Candidate Folders (N):"))
        self.candidate_list = QListWidget()
        self.candidate_list.setSelectionMode(QAbstractItemView.MultiSelection)
        candidate_vbox.addWidget(self.candidate_list)
        
        folders_layout.addLayout(source_vbox)
        folders_layout.addLayout(candidate_vbox)
        
        folders_box.addWidget(folders_label)
        folders_box.addLayout(folders_layout)
        layout.addLayout(folders_box)

        # 3. Start Button
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
        self.source_list.clear()
        self.candidate_list.clear()
        
        folders = self.data_loader.get_subfolders()
        self.source_list.addItems(folders)
        self.candidate_list.addItems(folders)
        
        self.source_list.currentItemChanged.connect(self.filter_candidates)
        self.btn_start.setEnabled(len(folders) > 0)

    def filter_candidates(self, current, previous):
        if current:
            source_folder = current.text()
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
        
        # Call the callback to transition to the next window
        self.on_start_callback(source_folder, candidate_folders)
