import os
import shutil
from pathlib import Path
from src.core.data_loader import DataLoader

def setup_test_data(root_path: Path):
    """Creates a dummy directory structure for testing."""
    if root_path.exists():
        shutil.rmtree(root_path)
    
    # Define folders and files
    # source: img1, img2, img3
    # haze: img1 (png), img2 (png) -> missing img3
    # low: img1 (jpg), img3 (jpg) -> missing img2
    # other: img1.txt (should be ignored)
    
    structure = {
        "source": ["img1.jpg", "img2.jpg", "img3.jpg"],
        "haze": ["img1.png", "img2.png"],
        "low": ["img1.jpg", "img3.jpg"],
        "other": ["img1.txt", "img2.txt"]
    }
    
    for folder, files in structure.items():
        folder_path = root_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        for file in files:
            (folder_path / file).touch()
    
    print(f"✅ Test data created at {root_path}")

def test_data_loader():
    test_root = Path("pikfix/tests/test_data")
    setup_test_data(test_root)
    
    # We need to be in the pikfix directory for the DataLoader to work with relative paths
    # or we pass the absolute path.
    loader = DataLoader(str(test_root))
    
    print("\n--- Testing get_subfolders ---")
    folders = loader.get_subfolders()
    print(f"Found folders: {folders}")
    assert set(folders) == {"source", "haze", "low", "other"}, "Subfolders mismatch!"
    print("✅ get_subfolders passed")

    print("\n--- Testing match_images ---")
    # Match source with haze and low
    results = loader.match_images("source", ["haze", "low"])
    print(f"Matched sets: {len(results)}")
    
    # Expecting 3 sets (img1, img2, img3)
    assert len(results) == 3, f"Expected 3 matched sets, got {len(results)}"
    
    # Verify img1: has both haze and low
    img1 = next(item for item in results if item['stem'] == 'img1')
    assert 'haze' in img1['candidates'] and 'low' in img1['candidates'], "img1 should have both candidates"
    
    # Verify img2: has haze, missing low
    img2 = next(item for item in results if item['stem'] == 'img2')
    assert 'haze' in img2['candidates'] and 'low' not in img2['candidates'], "img2 should only have haze"
    
    # Verify img3: missing haze, has low
    img3 = next(item for item in results if item['stem'] == 'img3')
    assert 'haze' not in img3['candidates'] and 'low' in img3['candidates'], "img3 should only have low"
    
    print("✅ match_images passed")
    print("\n🚀 ALL LOGIC TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    # Since we are running from the workspace root, 
    # we need to ensure the python path includes the 'pikfix' directory
    import sys
    sys.path.append(os.path.abspath("pikfix"))
    
    try:
        test_data_loader()
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
