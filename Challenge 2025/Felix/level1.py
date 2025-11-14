from pathlib import Path


class DataLevelLoader:
    def __init__(self, level: int, base_path=None):
        """Initialize the DataLevelLoader for a specific level."""
        self.level = level
        if base_path is None:
            # Default to Challenge 2025 directory
            self.base_path = Path(__file__).parent.parent
        else:
            self.base_path = Path(base_path)
        self.input_dir = self.base_path / "Input" / f"level{level}"
        self.output_dir = self.base_path / "Felix" / "Outputs" / f"level{level}"

    def load_input_files(self):
        """Load all .in files from the input directory."""
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")

        input_files = list(self.input_dir.glob("*.in"))
        if not input_files:
            raise FileNotFoundError(f"No .in files found in {self.input_dir}")

        return sorted(input_files)

    def process_level1(self, input_file):
        """
        Process a level1 input file.
        - Read the first number (number of sequences)
        - Ignore the first number
        - Calculate the sum of all numbers in the remaining lines
        - Return the sum
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Parse the first line to get the number of sequences
        first_line = lines[0].strip()
        # Format: "1�3" - the first number is the count
        parts = first_line.split('�')
        num_sequences = int(parts[0].strip())

        total_sum = 0

        # Process lines 2 to num_sequences + 1 (skipping the first line)
        for i in range(1, num_sequences + 1):
            if i < len(lines):
                line = lines[i].strip()
                # Format: "2�5 5" - extract numbers after the arrow
                if '�' in line:
                    arrow_parts = line.split('�')
                    numbers_str = arrow_parts[1].strip()

                    if numbers_str:  # Only sum if there are numbers
                        numbers = [int(n) for n in numbers_str.split()]
                        total_sum += sum(numbers)

        return total_sum

    def process_and_save(self):
        """Process all input files and generate output files."""
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        input_files = self.load_input_files()

        for input_file in input_files:
            try:
                result = self.process_level1(input_file)

                # Generate output filename
                output_filename = input_file.stem + ".out"
                output_file = self.output_dir / output_filename

                # Write result to output file
                with open(output_file, 'w') as f:
                    f.write(str(result))

                print(f" Processed {input_file.name} � {output_filename} (Result: {result})")

            except Exception as e:
                print(f" Error processing {input_file.name}: {e}")


def main():
    """Main entry point for the script."""
    loader = DataLevelLoader(level=1)
    loader.process_and_save()


if __name__ == "__main__":
    main()
