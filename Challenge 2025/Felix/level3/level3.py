from class_Data_Level_loader import DataLevelLoader


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
            # Move forward by 1
            position += 1
            total_time += pace  # time cost equals pace magnitude
        elif pace < 0:
            # Move backward by 1
            position -= 1
            total_time += abs(pace)  # abs(pace)
        else:
            # Stand still: no space change, but 1 time unit
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
    
    Rules:
    - Start and end at pace 0
    - From pace 0, can ONLY jump to ±5 (not to any other pace)
    - To pace 0, can ONLY jump from ±5 (not from any other pace)
    - When pace is non-zero, can only change by ±1 each step
    - At pace P (P ≠ 0): move by sign(P)*1, costs abs(P) time units
    
    Strategy: Use pace 1 (fastest) for large distances with tight time limits
    - 0 → 5 → 4 → 3 → 2 → 1 → (stay at 1) → 2 → 3 → 4 → 5 → 0
    """
    
    if target_position == 0:
        return "0"
    
    direction = 1 if target_position > 0 else -1
    target = abs(target_position)
    
    sequence = [0]
    
    # Special cases for very small targets
    if target == 1:
        sequence.extend([5 * direction, 0])
        valid, msg = validate_sequence(sequence, target_position, time_limit)
        if not valid:
            raise ValueError(f"Generated invalid sequence for pos={target_position}: {msg}")
        return ' '.join(map(str, sequence))
    elif target == 2:
        sequence.extend([5 * direction, 5 * direction, 0])
        valid, msg = validate_sequence(sequence, target_position, time_limit)
        if not valid:
            raise ValueError(f"Generated invalid sequence for pos={target_position}: {msg}")
        return ' '.join(map(str, sequence))
    
    # For targets >= 9, use pace 1 (fastest, minimal time cost)
    # Pattern: 0 → 5 → 4 → 3 → 2 → 1 → (stay at 1) → 2 → 3 → 4 → 5 → 0
    # Ramp down: 5→4→3→2→1 = 5 moves, time = 5+4+3+2+1 = 15
    # Stay at 1: N moves, time = N
    # Ramp up: 2→3→4→5 = 4 moves, time = 2+3+4+5 = 14
    # Total: 9 + N moves, 29 + N time
    
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
        valid, msg = validate_sequence(sequence, target_position, time_limit)
        if not valid:
            raise ValueError(f"Generated invalid sequence for pos={target_position}: {msg}")
        return ' '.join(map(str, sequence))
    
    # For smaller targets (3-8), use symmetric valley pattern or adjusted pattern
    # Valley depths: min_pace=3 gives 5 moves, min_pace=2 gives 7 moves, etc.
    # These give odd numbers: 1, 3, 5, 7, 9
    
    # Check for exact match with valley pattern
    for min_pace in range(5, 0, -1):
        valley_moves = 2 * (5 - min_pace) + 1
        
        if valley_moves == target:
            # Use this valley
            for pace in range(5, min_pace - 1, -1):
                sequence.append(pace * direction)
            for pace in range(min_pace + 1, 6):
                sequence.append(pace * direction)
            sequence.append(0)
            valid, msg = validate_sequence(sequence, target_position, time_limit)
            if not valid:
                raise ValueError(f"Generated invalid sequence for pos={target_position}: {msg}")
            return ' '.join(map(str, sequence))
    
    # For even numbers (4, 6, 8), use valley + one extra move at pace 5
    # Example: target=4 → use valley of 3 moves + 1 extra at pace 5
    # Pattern: 0 → 5 → 5 → 4 → 5 → 0 (gives 4 moves)
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
            valid, msg = validate_sequence(sequence, target_position, time_limit)
            if not valid:
                raise ValueError(f"Generated invalid sequence for pos={target_position}: {msg}")
            return ' '.join(map(str, sequence))
    
    # Should not reach here
    raise ValueError(f"Cannot generate sequence for position {target_position}")


def solve_level3(input_file, output_file):
    """Solve a single level 3 input file."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    n = int(lines[0].strip())
    results = []
    
    for i in range(1, n + 1):
        position, time_limit = map(int, lines[i].strip().split())
        sequence = generate_sequence(position, time_limit)
        results.append(sequence)
    
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')


def main():
    """Main function to process all level 3 input files."""
    loader = DataLevelLoader(level=3)
    input_files = loader.load_input_files()
    output_dir = loader.get_output_dir()
    
    print(f"Processing {len(input_files)} input files for Level 3")
    
    for input_file in input_files:
        output_file = output_dir / input_file.name.replace('.in', '.out')
        print(f"Processing {input_file.name}...")
        solve_level3(input_file, output_file)
        print(f"  Output written to {output_file}")
    
    print("Done!")


if __name__ == "__main__":
    main()