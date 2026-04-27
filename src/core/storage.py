import json
from pathlib import Path
from typing import Dict, Any, List

class ProgressManager:
    """
    Handles saving and loading the user's progress and GT selections.
    """
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.progress_file = self.root_path / "review_progress.json"
        self.manifest_file = self.root_path / "final_gt" / "manifest.json"

    def save_progress(self, current_index: int, selections: Dict[str, str]):
        """
        Saves the current index and the mapping of {stem: selected_folder}.
        """
        data = {
            "current_index": current_index,
            "selections": selections
        }
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        # Also update the manifest file for external analysis
        # Ensure directory exists
        self.manifest_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(selections, f, indent=4)

    def load_progress(self) -> Dict[str, Any]:
        """Loads the saved progress. Returns default values if no file exists."""
        if not self.progress_file.exists():
            return {"current_index": 0, "selections": {}}
        
        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"current_index": 0, "selections": {}}

    def clear_progress(self):
        """Deletes the progress and manifest files to start over."""
        if self.progress_file.exists():
            self.progress_file.unlink()
        if self.manifest_file.exists():
            self.manifest_file.unlink()
