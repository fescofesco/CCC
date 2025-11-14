import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from pathlib import Path


class DataLevelLoader:
    def __init__(self, level: int, base_path=None):
        """Initialize the DataLevelLoader for a specific level."""
        self.level = level
        if base_path is None:
            # Default to Challenge 2025 directory
            # This file is in Challenge 2025/Felix/level4/
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


def calculate_position_and_time(sequence):
    """
    Calculate position and time using level2 logic.
    
    Args:
        sequence: List of pace integers
    
    Returns:
        tuple: (position, total_time)
    """
    position = 0
    total_time = 0
    
    for pace in sequence:
        if pace > 0:
            position += 1
            total_time += pace
        elif pace < 0:
            position -= 1
            total_time += abs(pace)
        else:
            total_time += 1
    
    return position, total_time


def validate_sequence(sequence, expected_position, time_limit):
    """
    Validate a sequence against all rules.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Rule 1: Start and end with 0
    if sequence[0] != 0:
        return False, f"Does not start with 0"
    if sequence[-1] != 0:
        return False, f"Does not end with 0"
    
    # Rule 2: From 0, can only go to ±5
    for i in range(len(sequence) - 1):
        if sequence[i] == 0 and sequence[i+1] != 0:
            if abs(sequence[i+1]) != 5:
                return False, f"From 0 to {sequence[i+1]} (must be ±5)"
    
    # Rule 3: To 0, can only come from ±5
    for i in range(len(sequence) - 1):
        if sequence[i] != 0 and sequence[i+1] == 0:
            if abs(sequence[i]) != 5:
                return False, f"To 0 from {sequence[i]} (must be ±5)"
    
    # Rule 4: Between non-zero paces, can only change by ±1
    for i in range(len(sequence) - 1):
        if sequence[i] != 0 and sequence[i+1] != 0:
            diff = abs(sequence[i+1] - sequence[i])
            if diff > 1:
                return False, f"Pace {sequence[i]} to {sequence[i+1]} (change > 1)"
    
    # Rule 5: Pace range is ±1 to ±5
    for pace in sequence:
        if abs(pace) > 5:
            return False, f"Pace {pace} exceeds maximum (±5)"
    
    # Calculate position and time
    position, time_used = calculate_position_and_time(sequence)
    
    if position != expected_position:
        return False, f"Position {position} != {expected_position}"
    
    if time_used > time_limit:
        return False, f"Time {time_used} > {time_limit}"
    
    return True, f"Valid (pos={position}, time={time_used}/{time_limit})"


def generate_sequence(target_position, time_limit):
    """
    Generate a pace sequence to reach target_position within time_limit.
    
    Uses the same logic as level3 but optimized for time efficiency.
    """
    
    if target_position == 0:
        return [0]
    
    direction = 1 if target_position > 0 else -1
    target = abs(target_position)
    
    sequence = [0]
    
    # Special cases for very small targets
    if target == 1:
        sequence.extend([5 * direction, 0])
        return sequence
    elif target == 2:
        sequence.extend([5 * direction, 5 * direction, 0])
        return sequence
    
    # For targets >= 9, use pace 1 (fastest, minimal time cost)
    if target >= 9:
        extra_moves_at_1 = target - 9
        
        # Ramp down from 5 to 1
        for pace in range(5, 0, -1):
            sequence.append(pace * direction)
        
        # Stay at pace 1
        for _ in range(extra_moves_at_1):
            sequence.append(1 * direction)
        
        # Ramp up from 2 to 5
        for pace in range(2, 6):
            sequence.append(pace * direction)
        
        sequence.append(0)
        return sequence
    
    # For smaller targets (3-8), use symmetric valley pattern
    # Check for exact match with valley pattern (odd numbers: 1, 3, 5, 7, 9)
    for min_pace in range(5, 0, -1):
        valley_moves = 2 * (5 - min_pace) + 1
        
        if valley_moves == target:
            # Use this valley
            for pace in range(5, min_pace - 1, -1):
                sequence.append(pace * direction)
            for pace in range(min_pace + 1, 6):
                sequence.append(pace * direction)
            sequence.append(0)
            return sequence
    
    # For even numbers (4, 6, 8), use valley + one extra move at pace 5
    for min_pace in range(5, 0, -1):
        valley_moves = 2 * (5 - min_pace) + 1
        
        if valley_moves == target - 1:
            # Add one extra move at pace 5
            sequence.append(5 * direction)
            sequence.append(5 * direction)  # Extra move
            for pace in range(4, min_pace - 1, -1):
                sequence.append(pace * direction)
            for pace in range(min_pace + 1, 6):
                sequence.append(pace * direction)
            sequence.append(0)
            return sequence
    
    # Should not reach here
    raise ValueError(f"Cannot generate sequence for position {target_position}")


def solve_level4(input_file, output_file):
    """Solve a single level 4 input file."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    n = int(lines[0].strip())
    results = []
    
    for i in range(1, n + 1):
        line = lines[i].strip()
        # Parse "x,y time_limit"
        pos_part, time_limit_str = line.split()
        x_pos, y_pos = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        
        # Generate sequences for X and Y independently
        x_sequence = generate_sequence(x_pos, time_limit)
        y_sequence = generate_sequence(y_pos, time_limit)
        
        # Validate both sequences
        x_valid, x_msg = validate_sequence(x_sequence, x_pos, time_limit)
        if not x_valid:
            raise ValueError(f"Invalid X sequence for ({x_pos},{y_pos}): {x_msg}")
        
        y_valid, y_msg = validate_sequence(y_sequence, y_pos, time_limit)
        if not y_valid:
            raise ValueError(f"Invalid Y sequence for ({x_pos},{y_pos}): {y_msg}")
        
        # Format output: X-sequence on one line, Y-sequence on next line, blank line
        x_seq_str = ' '.join(map(str, x_sequence))
        y_seq_str = ' '.join(map(str, y_sequence))
        
        results.append(x_seq_str)
        results.append(y_seq_str)
        results.append('')  # Blank line between cases
    
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')


def main():
    """Main function to process all level 4 input files."""
    loader = DataLevelLoader(level=4)
    input_files = loader.load_input_files()
    output_dir = loader.get_output_dir()
    
    print(f"Processing {len(input_files)} input files for Level 4")
    
    for input_file in input_files:
        output_file = output_dir / input_file.name.replace('.in', '.out')
        print(f"Processing {input_file.name}...")
        try:
            solve_level4(input_file, output_file)
            print(f"  Output written to {output_file}")
        except Exception as e:
            print(f"  ERROR: {e}")
            raise
    
    print("Done!")


if __name__ == "__main__":
    main()
