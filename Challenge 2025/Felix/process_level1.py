#!/usr/bin/env python3
"""
Standalone script to process level1 .in files and generate .out files
"""
from pathlib import Path


def process_level1_file(input_file_path):
    """
    Process a single level1 input file.
    Returns the sum of all numbers in the file (excluding the first count number).
    """
    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        return 0

    # Parse the first line to get the number of sequences
    first_line = lines[0].strip()
    try:
        # Format: "1→3" - extract the number before the arrow
        parts = first_line.split('→')
        num_sequences = int(parts[0].strip())
    except (IndexError, ValueError):
        return 0

    total_sum = 0

    # Process the next num_sequences lines
    for i in range(1, min(num_sequences + 1, len(lines))):
        line = lines[i].strip()
        if '→' in line:
            try:
                # Extract the part after the arrow
                arrow_parts = line.split('→')
                numbers_str = arrow_parts[1].strip()

                # Sum all numbers on this line
                if numbers_str:
                    numbers = [int(n) for n in numbers_str.split()]
                    total_sum += sum(numbers)
            except (ValueError, IndexError):
                # Skip lines with parsing errors
                continue

    return total_sum


def main():
    """Main processing function."""
    # Paths
    base_path = Path(__file__).parent.parent
    input_dir = base_path / "Input" / "level1"
    output_dir = base_path / "Felix" / "Outputs" / "level1"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all .in files
    input_files = sorted(input_dir.glob("*.in"))

    if not input_files:
        print(f"No .in files found in {input_dir}")
        return

    # Process each file
    results = []
    for input_file in input_files:
        try:
            result = process_level1_file(input_file)

            # Generate output filename
            output_filename = input_file.stem + ".out"
            output_file = output_dir / output_filename

            # Write result to output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(result))

            message = f"✓ {input_file.name} → {output_filename} (Result: {result})"
            results.append(message)
            print(message)

        except Exception as e:
            message = f"✗ Error processing {input_file.name}: {e}"
            results.append(message)
            print(message)

    # Write summary
    summary_file = output_dir / "PROCESSING_SUMMARY.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Level 1 Processing Summary\n")
        f.write("=" * 50 + "\n\n")
        for msg in results:
            f.write(msg + "\n")
        f.write(f"\nProcessed {len(input_files)} files\n")
        f.write(f"Output directory: {output_dir}\n")

    print(f"\nProcessing complete! Summary saved to {summary_file}")


if __name__ == "__main__":
    main()
