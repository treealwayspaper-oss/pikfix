from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QFrame
from PySide6.QtGui import QPixmap, QColor, QFont
from PySide6.QtCore import Qt, Signal

class DynamicImageLabel(QLabel):
    """
    A QLabel that automatically scales its pixmap to fit the current size
    while maintaining the aspect ratio.
    """
    doubleClicked = Signal(str)

    def __init__(self, pixmap=None, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.image_path = None
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(1, 1)
        self.update_pixmap()

    def set_pixmap(self, pixmap, path=None):
        self.pixmap = pixmap
        self.image_path = path
        self.update_pixmap()

    def update_pixmap(self):
        if self.pixmap:
            scaled = self.pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
        else:
            self.setPixmap(QPixmap())

    def resizeEvent(self, event):
        self.update_pixmap()
        super().resizeEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.image_path:
            self.doubleClicked.emit(self.image_path)
        super().mouseDoubleClickEvent(event)

class ImageCandidateWidget(QFrame):
    """
    A widget to display a candidate image. 
    Selection is managed by the parent ReviewWindow.
    """
    clicked = Signal(str) # Signal to notify selection request
    doubleClicked = Signal(str) # Signal to notify double click

    def __init__(self, folder_name, image_path, parent=None):
        super().__init__(parent)
        self.folder_name = folder_name
        self.image_path = image_path
        self._is_selected = False
        
        # Use a fixed line width to prevent layout shifts when selecting
        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(2) 
        self.update_style()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        self.image_label = DynamicImageLabel(QPixmap(str(image_path)))
        self.image_label.set_pixmap(QPixmap(str(image_path)), str(image_path))
        self.image_label.doubleClicked.connect(self.on_image_double_clicked)
        
        # Folder name label with larger, more legible font
        self.name_label = QLabel(folder_name)
        self.name_label.setAlignment(Qt.AlignCenter)
        font = self.name_label.font()
        font.setPointSize(11) # Increased font size
        font.setBold(True)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet("color: #333;")
        
        layout.addWidget(self.image_label, 1)
        layout.addWidget(self.name_label)
        
    def set_selected(self, selected: bool):
        """Explicitly set the selection state and update style."""
        self._is_selected = selected
        self.update_style()

    def update_style(self):
        if self._is_selected:
            # Fixed 2px border to prevent layout jumps
            self.setStyleSheet("border: 2px solid #4CAF50; background-color: #E8F5E9;")
        else:
            self.setStyleSheet("border: 2px solid #DDD; background-color: transparent;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.folder_name)
        super().mousePressEvent(event)

    def on_image_double_clicked(self, path):
        self.doubleClicked.emit(path)
