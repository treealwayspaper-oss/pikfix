from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class BBox:
    """
    Bounding Box representation.
    Coordinates are normalized (0.0 to 1.0) relative to image size.
    """
    x: float  # Top-left x
    y: float  # Top-left y
    width: float
    height: float
    label: str

@dataclass
class Polygon:
    """
    Polygon representation for segmentation.
    Points are normalized (0.0 to 1.0) relative to image size.
    """
    points: List[Tuple[float, float]] # List of (x, y) pairs
    label: str

@dataclass
class ImageAnnotation:
    """
    Internal representation of all annotations for a single image.
    """
    image_name: str
    width: int
    height: int
    bboxes: List[BBox] = field(default_factory=list)
    polygons: List[Polygon] = field(default_factory=list)

    def add_bbox(self, x: float, y: float, w: float, h: float, label: str):
        self.bboxes.append(BBox(x, y, w, h, label))

    def add_polygon(self, points: List[Tuple[float, float]], label: str):
        self.polygons.append(Polygon(points, label))
