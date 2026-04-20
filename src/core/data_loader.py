import os
from pathlib import Path
from typing import List, Dict, Set, Tuple

class DataLoader:
    """
    Handles scanning of data directories and matching of source images 
    with their corresponding candidate Ground Truth (GT) images.
    """
    
    def __init__(self, root_path: str = ""):
        self.root_path = Path(root_path)
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tif', '.tiff'}

    def get_subfolders(self) -> List[str]:
        """Returns a list of subdirectories in the root path."""
        if not self.root_path.exists() or not self.root_path.is_dir():
            return []
        
        return [f.name for f in self.root_path.iterdir() if f.is_dir()]

    def _get_image_files(self, folder_path: Path) -> Dict[str, Path]:
        """
        Returns a mapping of {stem: full_path} for all supported images in a folder.
        Example: {'image1': Path('.../source/image1.jpg')}
        """
        images = {}
        if not folder_path.exists() or not folder_path.is_dir():
            return images
            
        for file in folder_path.iterdir():
            if file.suffix.lower() in self.supported_extensions:
                images[file.stem] = file
        return images

    def match_images(self, source_folder_name: str, candidate_folder_names: List[str]) -> List[Dict]:
        """
        Matches source images with candidates based on their stems.
        
        Returns:
            A list of dictionaries:
            [
                {
                    'stem': 'image1',
                    'source': Path('.../source/image1.jpg'),
                    'candidates': {
                        'haze': Path('.../haze/image1.png'),
                        'low': Path('.../low/image1.jpg')
                    }
                },
                ...
            ]
        """
        source_path = self.root_path / source_folder_name
        source_images = self._get_image_files(source_path)
        
        # Prepare candidate mappings
        candidate_maps = {}
        for folder in candidate_folder_names:
            path = self.root_path / folder
            candidate_maps[folder] = self._get_image_files(path)
            
        matched_data = []
        
        # Iterate through source images and find corresponding candidates
        for stem, source_file in source_images.items():
            candidates = {}
            for folder, images in candidate_maps.items():
                if stem in images:
                    candidates[folder] = images[stem]
            
            # We only add to the list if it has a source image (guaranteed here)
            # and optionally we could filter out those with no candidates, 
            # but for a review tool, showing an image with no candidates might be useful.
            matched_data.append({
                'stem': stem,
                'source': source_file,
                'candidates': candidates
            })
            
        # Sort by stem to ensure consistent order
        matched_data.sort(key=lambda x: x['stem'])
        
        return matched_data
