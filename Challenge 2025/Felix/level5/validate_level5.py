import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from pathlib import Path


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
    """Validate a sequence against all movement rules."""
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


def validate_level5_file(input_file, output_file):
    """Validate a single level 5 output file (sequences only, not collision)."""
    # Read input
    with open(input_file, 'r') as f:
        input_lines = f.readlines()
    
    # Read output
    with open(output_file, 'r') as f:
        output_lines = f.readlines()
    
    n = int(input_lines[0].strip())
    
    errors = []
    
    for i in range(n):
        # Parse input
        station_line = input_lines[1 + i * 2].strip()
        
        pos_part, time_limit_str = station_line.split()
        target_x, target_y = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        
        # Parse output (each case is 3 lines: X sequence, Y sequence, blank)
        x_seq_line = output_lines[i * 3].strip()
        y_seq_line = output_lines[i * 3 + 1].strip()
        
        if not x_seq_line or not y_seq_line:
            print(f"  Case {i+1}: ERROR - Empty sequence")
            errors.append(f"Case {i+1}: Empty sequence")
            continue
        
        x_sequence = list(map(int, x_seq_line.split()))
        y_sequence = list(map(int, y_seq_line.split()))
        
        # Validate X sequence
        x_valid, x_msg = validate_sequence(x_sequence, target_x, time_limit)
        if not x_valid:
            print(f"  Case {i+1}: X sequence INVALID - {x_msg}")
            errors.append(f"Case {i+1} X: {x_msg}")
        
        # Validate Y sequence
        y_valid, y_msg = validate_sequence(y_sequence, target_y, time_limit)
        if not y_valid:
            print(f"  Case {i+1}: Y sequence INVALID - {y_msg}")
            errors.append(f"Case {i+1} Y: {y_msg}")
        
        # Check sequence lengths match
        if len(x_sequence) != len(y_sequence):
            print(f"  Case {i+1}: ERROR - Sequence lengths don't match (X={len(x_sequence)}, Y={len(y_sequence)})")
            errors.append(f"Case {i+1}: Length mismatch")
        
        if x_valid and y_valid and len(x_sequence) == len(y_sequence):
            print(f"  Case {i+1}: OK - Both sequences valid")
    
    return errors


def main():
    """Main function to validate all level 5 output files."""
    # Get paths
    base_path = Path(__file__).parent.parent.parent
    input_dir = base_path / "Input" / "level5"
    output_dir = base_path / "Felix" / "Outputs" / "level5"
    
    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}")
        return
    
    if not output_dir.exists():
        print(f"ERROR: Output directory not found: {output_dir}")
        return
    
    input_files = sorted(input_dir.glob("*.in"))
    
    print(f"Validating {len(input_files)} level 5 output files (sequence validation)")
    print("=" * 70)
    
    all_valid = True
    
    for input_file in input_files:
        output_file = output_dir / input_file.name.replace('.in', '.out')
        
        if not output_file.exists():
            print(f"\n{input_file.name}: Output file not found")
            all_valid = False
            continue
        
        print(f"\n{input_file.name}:")
        
        try:
            errors = validate_level5_file(input_file, output_file)
            
            if errors:
                all_valid = False
                print(f"  FAILED: {len(errors)} error(s)")
            else:
                print(f"  PASSED: All sequences valid")
        
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            all_valid = False
    
    print("\n" + "=" * 70)
    if all_valid:
        print("✓ All files passed sequence validation!")
    else:
        print("✗ Some files have invalid sequences")


if __name__ == "__main__":
    main()
