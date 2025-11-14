from pathlib import Path
from level1 import DataLevelLoader

if __name__ == "__main__":
    try:
        loader = DataLevelLoader(1)

        # Debug output
        with open("debug.txt", "w") as f:
            f.write(f"Base path: {loader.base_path}\n")
            f.write(f"Input dir: {loader.input_dir}\n")
            f.write(f"Input dir exists: {loader.input_dir.exists()}\n")

        # Process files
        loader.process_and_save()

        # Write success
        with open("success.txt", "w") as f:
            f.write("Processing completed!")

    except Exception as e:
        with open("error.txt", "w") as f:
            f.write(f"Error: {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())
