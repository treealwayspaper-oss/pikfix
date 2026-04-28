import os
from pathlib import Path
from src.core.annotations.models import ImageAnnotation, BBox, Polygon
from src.core.annotations.converter import AnnotationConverter

def test_yolo_conversion():
    print("Testing YOLO Conversion...")
    # Setup
    class_map = {"dog": 0, "cat": 1}
    class_map_inv = {0: "dog", 1: "cat"}
    
    anno = ImageAnnotation("test.jpg", 1000, 1000)
    anno.add_bbox(0.1, 0.1, 0.2, 0.2, "dog") # x=100, y=100, w=200, h=200 -> center=200, 200
    
    # To YOLO
    yolo_out = AnnotationConverter.to_yolo(anno, class_map)
    expected = "0 0.200000 0.200000 0.200000 0.200000"
    assert yolo_out == expected, f"YOLO output mismatch: {yolo_out} != {expected}"
    print("✅ YOLO Export passed")
    
    # From YOLO
    yolo_in = "1 0.5 0.5 0.1 0.1"
    anno_back = AnnotationConverter.from_yolo("test.jpg", 1000, 1000, yolo_in, class_map_inv)
    assert anno_back.bboxes[0].label == "cat"
    assert anno_back.bboxes[0].x == 0.45 # 0.5 - 0.1/2
    print("✅ YOLO Import passed")

def test_coco_conversion():
    print("\nTesting COCO Conversion...")
    class_map = {"dog": 0}
    image_id_map = {"test.jpg": 1}
    
    anno = ImageAnnotation("test.jpg", 100, 100)
    anno.add_bbox(0.1, 0.1, 0.2, 0.2, "dog")
    anno.add_polygon([(0.1, 0.1), (0.2, 0.1), (0.2, 0.2), (0.1, 0.2)], "dog")
    
    coco_out = AnnotationConverter.to_coco([anno], class_map, image_id_map)
    
    assert coco_out["images"][0]["file_name"] == "test.jpg"
    assert coco_out["annotations"][0]["bbox"] == [10.0, 10.0, 20.0, 20.0]
    assert coco_out["annotations"][1]["segmentation"][0] == [10.0, 10.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0]
    print("✅ COCO Export passed")

if __name__ == "__main__":
    try:
        test_yolo_conversion()
        test_coco_conversion()
        print("\n🚀 ALL ANNOTATION TESTS PASSED!")
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
