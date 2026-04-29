from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from ui.selection_window import SelectionWindow
# To be implemented in Phase 2: from ui.annotation_window import AnnotationWindow

class ModeManager:
    """
    Manages the transition between different operation modes in PikFix.
    """
    def __init__(self, main_window: QMainWindow, data_loader):
        self.main_window = main_window
        self.data_loader = data_loader
        self.current_window = None

    def launch_selection_mode(self, source_folder: str, candidate_folders: list):
        """Launches the GT Selection interface."""
        if self.current_window:
            self.current_window.close()
            
        root_path = str(self.data_loader.root_path)
        
        try:
            matched_data = self.data_loader.match_images(source_folder, candidate_folders)
            if not matched_data:
                QMessageBox.warning(self.main_window, "Warning", "No matching images found.")
                return
            
            # Use root_path as output_path for now
            self.current_window = SelectionWindow(matched_data, root_path, root_path)
            self.current_window.show()
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to launch selection mode: {e}")

    def launch_annotation_mode(self):
        """Launches the Annotation interface (Placeholder for Phase 2)."""
        if self.current_window:
            self.current_window.close()
            
        QMessageBox.information(self.main_window, "Coming Soon", "Annotation Mode is currently under development (Phase 2).")
