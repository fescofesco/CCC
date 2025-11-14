from pathlib import Path


class DataLevelLoader:
    def __init__(self, level: int, base_path=None):
        """Initialize the DataLevelLoader for a specific level."""
        self.level = level
        if base_path is None:
            # Default to Challenge 2025 directory (go up two levels from this file)
            # This file is in Challenge 2025/Felix/level3/class_Data_Level_loader.py
            # We need to get to Challenge 2025/
            self.base_path = Path(__file__).parent.parent.parent
        else:
            self.base_path = Path(base_path)
        self.input_dir = self.base_path / "Input" / f"level{level}"
        self.output_dir = self.base_path / "Felix" / "Outputs" / f"level{level}"
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_input_files(self):
        """Load and return all .in files from the input directory."""
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")
        
        input_files = list(self.input_dir.glob("*.in"))
        if not input_files:
            raise FileNotFoundError(f"No .in files found in {self.input_dir}")
        
        return sorted(input_files)
    
    def get_output_dir(self):
        """Return the output directory path."""
        return self.output_dir