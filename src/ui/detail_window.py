from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtGui import QPixmap, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt

class ImageDetailWindow(QMainWindow):
    """
    A window that displays an image in high resolution and 
    allows the user to zoom and pan.
    """
    def __init__(self, image_path, title="Image Detail"):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(1000, 800)
        
        self.original_pixmap = QPixmap(str(image_path))
        self.scale_factor = 1.0
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area for panning
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.update_display()
        
        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)

    def update_display(self):
        # Scale original pixmap by the current scale factor
        scaled_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * self.scale_factor),
            int(self.original_pixmap.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setFixedSize(scaled_pixmap.size())

    def wheelEvent(self, event: QWheelEvent):
        """Handle zoom with mouse wheel."""
        delta = event.angleDelta().y()
        if delta > 0:
            self.scale_factor *= 1.2
        else:
            self.scale_factor *= 0.8
            
        # Clamp scale factor
        self.scale_factor = max(0.1, min(self.scale_factor, 10.0))
        self.update_display()
        super().wheelEvent(event)
