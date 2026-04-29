import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QFileDialog, QListWidget, 
    QLabel, QMessageBox, QAbstractItemView, QStackedWidget
)
from PySide6.QtCore import Qt
from core.data_loader import DataLoader
from ui.setup_page import SetupPage
from ui.mode_manager import ModeManager

class PikFixApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PikFix - AI Training Data Review Tool (v0.2)")
        self.resize(800, 600)
        
        self.data_loader = DataLoader()
        self.mode_manager = ModeManager(self, self.data_loader)
        self.setup_ui()

    def setup_ui(self):
        # Using QStackedWidget to manage different screens (Setup -> Mode Selection -> Window)
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)
        
        # Create the Setup Page
        self.setup_page = SetupPage(self.data_loader, self.on_start_requested)
        self.central_stack.addWidget(self.setup_page)

    def on_start_requested(self, source_folder, candidate_folders):
        """Callback called by SetupPage when the user wants to start a mode."""
        # Currently, we only have Selection Mode fully implemented.
        # The SetupPage now handles the mode selection logic internally or passes it here.
        # For the current implementation in setup_page.py, it simply calls this callback.
        
        # In a more advanced version, we would pass the selected mode as an argument.
        # For now, we default to launching Selection Mode.
        self.mode_manager.launch_selection_mode(source_folder, candidate_folders)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PikFixApp()
    window.show()
    sys.exit(app.exec())
