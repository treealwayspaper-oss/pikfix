import json
from pathlib import Path
from typing import List, Dict, Any
from .models import ImageAnnotation, BBox, Polygon

class AnnotationConverter:
    """
    Converter to translate between internal PikFix format 
    and industry standard formats (YOLO, COCO, VOC).
    """
    
    @staticmethod
    def to_yolo(annotation: ImageAnnotation, class_map: Dict[str, int]) -> str:
        """
        Converts internal BBox to YOLO format: <class_id> <x_center> <y_center> <width> <height>
        Note: YOLO only supports BBoxes.
        """
        lines = []
        for bbox in annotation.bboxes:
            class_id = class_map.get(bbox.label, 0)
            # Convert top-left to center
            x_center = bbox.x + bbox.width / 2
            y_center = bbox.y + bbox.height / 2
            lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox.width:.6f} {bbox.height:.6f}")
        
        return "\n".join(lines)

    @staticmethod
    def from_yolo(image_name: str, width: int, height: int, yolo_text: str, class_map_inv: Dict[int, str]) -> ImageAnnotation:
        """Converts YOLO text format back to internal representation."""
        anno = ImageAnnotation(image_name, width, height)
        for line in yolo_text.strip().split('\n'):
            if not line: continue
            parts = line.split()
            class_id = int(parts[0])
            xc, yc, w, h = map(float, parts[1:])
            
            # Convert center to top-left
            x = xc - w / 2
            y = yc - h / 2
            label = class_map_inv.get(class_id, "unknown")
            anno.add_bbox(x, y, w, h, label)
        return anno

    @staticmethod
    def to_coco(annotations: List[ImageAnnotation], class_map: Dict[str, int], image_id_map: Dict[str, int]) -> Dict[str, Any]:
        """
        Converts a list of internal annotations to COCO JSON format.
        """
        coco = {
            "images": [],
            "annotations": [],
            "categories": [{"id": v, "name": k} for k, v in class_map.items()]
        }
        
        ann_id = 0
        for anno in annotations:
            img_id = image_id_map.get(anno.image_name, 0)
            coco["images"].append({
                "id": img_id,
                "file_name": anno.image_name,
                "width": anno.width,
                "height": anno.height
            })
            
            # Process BBoxes
            for bbox in anno.bboxes:
                # COCO uses absolute pixels: [x, y, width, height]
                abs_x = bbox.x * anno.width
                abs_y = bbox.y * anno.height
                abs_w = bbox.width * anno.width
                abs_h = bbox.height * anno.height
                
                coco["annotations"].append({
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": class_map.get(bbox.label, 0),
                    "bbox": [abs_x, abs_y, abs_w, abs_h],
                    "area": abs_w * abs_h,
                    "iscrowd": 0,
                    "segmentation": []
                })
                ann_id += 1
            
            # Process Polygons
            for poly in anno.polygons:
                # COCO segmentation: [x1, y1, x2, y2, ...] absolute pixels
                abs_points = []
                for px, py in poly.points:
                    abs_points.append(px * anno.width)
                    abs_points.append(py * anno.height)
                
                coco["annotations"].append({
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": class_map.get(poly.label, 0),
                    "bbox": [], # Simplified for this example
                    "area": 0, # Simplified
                    "iscrowd": 0,
                    "segmentation": [abs_points]
                })
                ann_id += 1
                
        return coco
