import sys
import shutil
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QGridLayout, QMessageBox, QMainWindow
)
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import Qt
from ui.widgets import ImageCandidateWidget, DynamicImageLabel
from ui.detail_window import ImageDetailWindow
from core.storage import ProgressManager

class ReviewWindow(QMainWindow):
    """
    The main review window where the user compares the source image 
    with candidate images and selects the final GT.
    """
    def __init__(self, matched_data, root_path, output_path):
        super().__init__()
        self.matched_data = matched_data
        self.root_path = Path(root_path)
        self.output_path = Path(output_path) # User-defined output path
        
        # Setup progress manager for "Resume" feature
        self.progress_manager = ProgressManager(str(self.root_path))
        progress = self.progress_manager.load_progress()
        self.current_index = progress.get("current_index", 0)
        self.selections = progress.get("selections", {})
        
        # Setup final output directory
        self.output_dir = self.output_path / "final_gt"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.setWindowTitle("PikFix - Image Review")
        self.resize(1200, 800)
        
        self.setup_ui()
        self.load_current_set()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Header / Progress - Minimal height
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 5px;")
        main_layout.addWidget(self.progress_label)

        # 2. Main Content Area (Source + Candidates)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Left side: Source Image - Slimmer container
        source_container = QVBoxLayout()
        source_container.setContentsMargins(0, 0, 0, 0)
        source_container.setSpacing(5)
        
        source_title = QLabel("<b>Source</b>")
        source_title.setAlignment(Qt.AlignCenter)
        source_title.setStyleSheet("font-size: 12px; color: #555;")
        source_container.addWidget(source_title)
        
        self.source_image_display = DynamicImageLabel()
        self.source_image_display.doubleClicked.connect(self.open_detail_view)
        source_container.addWidget(self.source_image_display)
        
        content_layout.addLayout(source_container, 1)

        # Right side: Candidates Grid
        candidates_container = QVBoxLayout()
        candidates_container.setContentsMargins(0, 0, 0, 0)
        candidates_container.setSpacing(5)
        
        cand_title = QLabel("<b>Candidates</b>")
        cand_title.setAlignment(Qt.AlignCenter)
        cand_title.setStyleSheet("font-size: 12px; color: #555;")
        candidates_container.addWidget(cand_title)
        
        self.candidates_widget = QWidget()
        self.candidates_grid = QGridLayout(self.candidates_widget)
        self.candidates_grid.setSpacing(10)
        
        candidates_container.addWidget(self.candidates_widget)
        content_layout.addLayout(candidates_container, 3) # Candidates get 75% of width
        
        main_layout.addLayout(content_layout)

        # 3. Bottom Navigation & Action
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 10, 0, 0)
        
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.clicked.connect(self.prev_set)
        
        self.btn_save = QPushButton("Save Selected GT")
        self.btn_save.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; min-width: 150px;")
        self.btn_save.clicked.connect(self.save_gt)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(self.next_set)
        
        bottom_layout.addWidget(self.btn_prev)
        bottom_layout.addWidget(self.btn_save)
        bottom_layout.addWidget(self.btn_next)
        
        main_layout.addLayout(bottom_layout)

    def load_current_set(self):
        # Update progress
        self.progress_label.setText(f"Reviewing {self.current_index + 1} / {len(self.matched_data)}")
        
        # Clear candidates grid
        while self.candidates_grid.count():
            item = self.candidates_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        current_set = self.matched_data[self.current_index]
        
        # Load Source Image using DynamicImageLabel
        source_pixmap = QPixmap(str(current_set['source']))
        self.source_image_display.set_pixmap(source_pixmap)
        
        # Load Candidates with Dynamic Grid Calculation
        candidates = current_set['candidates']
        num_candidates = len(candidates)
        
        if num_candidates > 0:
            import math
            cols = math.ceil(math.sqrt(num_candidates))
            rows = math.ceil(num_candidates / cols)
            
            # Set equal stretch factors
            for c in range(cols):
                self.candidates_grid.setColumnStretch(c, 1)
            for r in range(rows):
                self.candidates_grid.setRowStretch(r, 1)
            
            for idx, (folder, path) in enumerate(candidates.items()):
                row = idx // cols
                col = idx % cols
                widget = ImageCandidateWidget(folder, path)
                widget.doubleClicked.connect(self.open_detail_view)
                widget.clicked.connect(self.handle_candidate_selection)
                
                # RESTORE previous selection if it exists
                stem = current_set['stem']
                if self.selections.get(stem) == folder:
                    widget.set_selected(True)
                
                self.candidates_grid.addWidget(widget, row, col)
        
        self.candidates_widget.update()
        
        # Update navigation button states
        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled(self.current_index < len(self.matched_data) - 1)

    def handle_candidate_selection(self, folder_name):
        """Ensures only one candidate is selected at a time."""
        for i in range(self.candidates_grid.count()):
            item = self.candidates_grid.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), ImageCandidateWidget):
                # Select only the one that matches the folder_name, and deselect others.
                item.widget().set_selected(item.widget().folder_name == folder_name)

    def save_gt(self):
        # Find which candidate was selected
        selected_widget = None
        for i in range(self.candidates_grid.count()):
            item = self.candidates_grid.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), ImageCandidateWidget):
                if item.widget()._is_selected:
                    selected_widget = item.widget()
                    break
        
        if not selected_widget:
            QMessageBox.warning(self, "Warning", "Please select a candidate GT first!")
            return
            
        # Saving logic
        current_set = self.matched_data[self.current_index]
        stem = current_set['stem']
        folder_name = selected_widget.folder_name
        src_path = selected_widget.image_path
        
        # 1. OVERRIDE Logic: Remove any previously saved GT for this stem
        # We look for any file in final_gt that starts with the stem
        for existing_file in self.output_dir.glob(f"{stem}_*"):
            existing_file.unlink()
        
        # 2. FILENAME Consistency: Save using ORIGINAL filename (stem + original ext)
        # This ensures the GT filenames match the source image filenames.
        ext = src_path.suffix
        dest_path = self.output_dir / f"{stem}{ext}"
        
        try:
            shutil.copy2(src_path, dest_path)
            
            # 3. Update Progress & Manifest
            # Update the mapping in self.selections
            self.selections[stem] = folder_name
            self.progress_manager.save_progress(self.current_index + 1, self.selections)
            
            self.next_set() # Auto move to next after saving
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts for efficient review."""
        key = event.key()
        
        # 1. Navigation: Left/Right Arrows
        if key == Qt.Key_Left:
            self.prev_set()
        elif key == Qt.Key_Right:
            self.next_set()
            
        # 2. Selection: Number keys 1-9
        elif Qt.Key_1 <= key <= Qt.Key_9:
            index = key - Qt.Key_1
            self.select_candidate_by_index(index)
            
        # 3. Save: Enter or S key
        elif key == Qt.Key_Return or key == Qt.Key_Enter or key == Qt.Key_S:
            self.save_gt()
            
        else:
            super().keyPressEvent(event)

    def select_candidate_by_index(self, index):
        """Selects a candidate GT by its grid index."""
        current_set = self.matched_data[self.current_index]
        candidates = list(current_set['candidates'].items())
        
        if index < len(candidates):
            target_folder = candidates[index][0]
            # Find the widget that matches this folder
            for i in range(self.candidates_grid.count()):
                item = self.candidates_grid.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), ImageCandidateWidget):
                    # Deselect others and select the target
                    is_target = item.widget().folder_name == target_folder
                    item.widget().set_selected(is_target)

    def next_set(self):
        if self.current_index < len(self.matched_data) - 1:
            self.current_index += 1
            self.load_current_set()
        else:
            QMessageBox.information(self, "Done", "You have reached the end of the dataset!")

    def prev_set(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_set()

    def open_detail_view(self, image_path):
        """Opens a high-resolution detail window for the selected image."""
        self.detail_window = ImageDetailWindow(image_path)
        self.detail_window.show()
