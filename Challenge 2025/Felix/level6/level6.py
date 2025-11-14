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
    """Calculate position and time using level2 logic."""
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
    """Validate a sequence against all rules."""
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
    """Generate a pace sequence to reach target_position within time_limit."""
    
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


def get_path_from_sequences(x_sequence, y_sequence):
    """
    Calculate the actual path taken by the spaceship over time.
    
    Each pace costs time: |pace| if pace≠0, or 1 if pace=0.
    X and Y move SIMULTANEOUSLY - when both dimensions have non-zero pace at the same time,
    they both move in the SAME time step (diagonal movement allowed).
    
    Returns list of (x, y) positions at each time step.
    """
    # Calculate total time needed
    x_time = sum(abs(p) if p != 0 else 1 for p in x_sequence)
    y_time = sum(abs(p) if p != 0 else 1 for p in y_sequence)
    max_time = max(x_time, y_time)
    
    path = []
    
    x_idx = 0
    x_pos = 0
    x_elapsed = 0
    
    y_idx = 0
    y_pos = 0
    y_elapsed = 0
    
    for t in range(max_time):
        # Move X if at start of pace
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            
            if x_elapsed == 0 and x_pace != 0:
                x_pos += 1 if x_pace > 0 else -1
            
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        # Move Y if at start of pace
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            
            if y_elapsed == 0 and y_pace != 0:
                y_pos += 1 if y_pace > 0 else -1
            
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
        
        # Record position after both dimensions have moved (if needed)
        path.append((x_pos, y_pos))
    
    return path


def check_asteroid_collision(path, asteroid_x, asteroid_y):
    """
    Check if the path collides with the asteroid's safety zone.
    
    The spaceship must stay MORE than 2 tiles away from the asteroid.
    This means Chebyshev distance must be > 2 (i.e., >= 3).
    
    Forbidden: any position where max(|x-ax|, |y-ay|) <= 2
    Including diagonal positions like (-5,2) when asteroid is at (-3,4).
    """
    
    for x, y in path:
        # Check Chebyshev distance (max of absolute differences)
        dx = abs(x - asteroid_x)
        dy = abs(y - asteroid_y)
        
        # Forbidden if BOTH dx <= 2 AND dy <= 2
        # This includes: (ax±2, ay), (ax, ay±2), (ax±1, ay±1), (ax±2, ay±2), etc.
        if dx <= 2 and dy <= 2:
            return True, f"Collision at ({x},{y}) - too close to asteroid at ({asteroid_x},{asteroid_y}) [dx={dx}, dy={dy}]"
    
    return False, "No collision"


def pad_sequences_to_avoid_asteroid(x_seq, y_seq, asteroid_x, asteroid_y, target_x, target_y, time_limit):
    """
    Pad sequences with zeros to avoid asteroid collision.
    Uses official validator logic to ensure collision-free paths.
    
    Strategy: Try multiple approaches in order:
    1. Original sequences (no padding needed)
    2. Delay one dimension (sequential movement)
    3. Detour strategies (go around asteroid)
    """
    # Import official validator to use exact collision detection
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'level5'))
    from official_validator import simulate_movement, check_asteroid_collision as official_check_collision
    
    def test_sequences(x_test, y_test):
        """Test if sequences are valid using official validator logic"""
        # Check time
        x_time = sum(max(1, abs(p)) for p in x_test)
        y_time = sum(max(1, abs(p)) for p in y_test)
        if x_time > time_limit or y_time > time_limit:
            return False
        
        # Check position
        x_pos = sum(1 if p > 0 else (-1 if p < 0 else 0) for p in x_test)
        y_pos = sum(1 if p > 0 else (-1 if p < 0 else 0) for p in y_test)
        if x_pos != target_x or y_pos != target_y:
            return False
        
        # Use official validator collision detection
        history = simulate_movement(x_test, y_test)
        collision, _, _, _ = official_check_collision(history, asteroid_x, asteroid_y)
        return not collision
    
    # Try original sequences
    max_len = max(len(x_seq), len(y_seq))
    x_padded = x_seq + [0] * (max_len - len(x_seq))
    y_padded = y_seq + [0] * (max_len - len(y_seq))
    
    if test_sequences(x_padded, y_padded):
        return x_padded, y_padded

    
    # Strategy 1: Move in Y first, then X (delay X)
    for extra_zeros in range(1, 150):
        x_test = [0] * extra_zeros + x_seq
        max_len = max(len(x_test), len(y_seq))
        x_padded = x_test + [0] * (max_len - len(x_test))
        y_padded = y_seq + [0] * (max_len - len(y_seq))
        
        if test_sequences(x_padded, y_padded):
            return x_padded, y_padded
    
    # Strategy 2: Move in X first, then Y (delay Y)
    for extra_zeros in range(1, 150):
        y_test = [0] * extra_zeros + y_seq
        max_len = max(len(x_seq), len(y_test))
        x_padded = x_seq + [0] * (max_len - len(x_seq))
        y_padded = y_test + [0] * (max_len - len(y_test))
        
        if test_sequences(x_padded, y_padded):
            return x_padded, y_padded
    
    
    # Strategy 3: Try detours - go past target, then return
    # Try X detours
    for extra in range(1, 20):
        for direction in [1, -1]:
            # Go extra units past target
            detour_target = target_x + extra * direction
            try:
                x_detour = generate_sequence(detour_target, time_limit)
            except:
                continue
            
            # Return path
            return_dist = abs(detour_target - target_x)
            return_dir = -1 if detour_target > target_x else 1
            x_return = [0]
            for _ in range(return_dist):
                x_return.append(5 * return_dir)
            x_return.append(0)
            
            # Combine: go, wait, return
            for y_wait in range(0, 50):
                x_combined = x_detour[:-1] + [0] * (len(y_seq) + y_wait - 2) + x_return[1:]
                y_combined = [0] * (len(x_detour) - 1) + [0] * y_wait + y_seq + [0] * (len(x_return) - 2)
                
                max_len = max(len(x_combined), len(y_combined))
                x_test = x_combined + [0] * (max_len - len(x_combined))
                y_test = y_combined + [0] * (max_len - len(y_combined))
                
                if test_sequences(x_test, y_test):
                    return x_test, y_test
    
    # Try Y detours
    for extra in range(1, 20):
        for direction in [1, -1]:
            detour_target = target_y + extra * direction
            try:
                y_detour = generate_sequence(detour_target, time_limit)
            except:
                continue
            
            return_dist = abs(detour_target - target_y)
            return_dir = -1 if detour_target > target_y else 1
            y_return = [0]
            for _ in range(return_dist):
                y_return.append(5 * return_dir)
            y_return.append(0)
            
            for x_wait in range(0, 50):
                y_combined = y_detour[:-1] + [0] * (len(x_seq) + x_wait - 2) + y_return[1:]
                x_combined = [0] * (len(y_detour) - 1) + [0] * x_wait + x_seq + [0] * (len(y_return) - 2)
                
                max_len = max(len(x_combined), len(y_combined))
                x_test = x_combined + [0] * (max_len - len(x_combined))
                y_test = y_combined + [0] * (max_len - len(y_combined))
                
                if test_sequences(x_test, y_test):
                    return x_test, y_test
    
    raise ValueError(f"Cannot find collision-free path to ({target_x},{target_y}) avoiding asteroid at ({asteroid_x},{asteroid_y})")


def solve_level6(input_file, output_file):
    """Solve a single level 6 input file."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    n = int(lines[0].strip())
    results = []
    
    for i in range(n):
        # Each case has 2 lines: station + time limit, then asteroid
        station_line = lines[1 + i * 2].strip()
        asteroid_line = lines[2 + i * 2].strip()
        
        # Parse station position and time limit
        pos_part, time_limit_str = station_line.split()
        target_x, target_y = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        
        # Parse asteroid position
        asteroid_x, asteroid_y = map(int, asteroid_line.split(','))
        
        # Generate base sequences
        x_sequence = generate_sequence(target_x, time_limit)
        y_sequence = generate_sequence(target_y, time_limit)
        
        # Pad and adjust to avoid asteroid
        try:
            x_padded, y_padded = pad_sequences_to_avoid_asteroid(
                x_sequence, y_sequence, asteroid_x, asteroid_y, target_x, target_y, time_limit
            )
            print(f"  Case {i+1}: Found collision-free path")
        except Exception as e:
            print(f"  Case {i+1} ERROR: {e}")
            # Use base sequences as fallback
            max_len = max(len(x_sequence), len(y_sequence))
            x_padded = x_sequence + [0] * (max_len - len(x_sequence))
            y_padded = y_sequence + [0] * (max_len - len(y_sequence))
        
        # Format output
        x_seq_str = ' '.join(map(str, x_padded))
        y_seq_str = ' '.join(map(str, y_padded))
        
        results.append(x_seq_str)
        results.append(y_seq_str)
        results.append('')  # Blank line between cases
    
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')


def main():
    """Main function to process all level 6 input files."""
    loader = DataLevelLoader(level=6)
    input_files = loader.load_input_files()
    output_dir = loader.get_output_dir()
    
    print(f"Processing {len(input_files)} input files for Level 6")
    
    for input_file in input_files:
        output_file = output_dir / input_file.name.replace('.in', '.out')
        print(f"Processing {input_file.name}...")
        try:
            solve_level6(input_file, output_file)
            print(f"  Output written to {output_file}")
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    print("Done!")


if __name__ == "__main__":
    main()
