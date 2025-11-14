import sys
import os

def validate_sequence(sequence, expected_position, time_limit):
    """
    Validate a sequence against all rules (adapted from Felix's solution).
    
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
    
    if position != expected_position:
        return False, f"Position {position} != {expected_position}"
    
    if total_time > time_limit:
        return False, f"Time {total_time} > {time_limit}"
    
    return True, f"Valid (pos={position}, time={total_time}/{time_limit})"

def find_optimal_sequence(target_pos, time_limit):
    """
    Generate a pace sequence to reach target_pos within time_limit.
    
    Rules (from Felix's solution):
    - Start and end at pace 0
    - From pace 0, can ONLY jump to ±5 (not to any other pace)
    - To pace 0, can ONLY jump from ±5 (not from any other pace)
    - When pace is non-zero, can only change by ±1 each step
    - At pace P (P ≠ 0): move by sign(P)*1, costs abs(P) time units
    
    Strategy: Use pace 1 (fastest) for large distances with tight time limits
    - 0 → 5 → 4 → 3 → 2 → 1 → (stay at 1) → 2 → 3 → 4 → 5 → 0
    """
    if target_pos == 0:
        return [0]
    
    direction = 1 if target_pos > 0 else -1
    target = abs(target_pos)
    
    sequence = [0]
    
    # Special cases for very small targets
    if target == 1:
        sequence.extend([5 * direction, 0])
        return sequence
    elif target == 2:
        sequence.extend([5 * direction, 5 * direction, 0])
        return sequence
    
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
        return sequence
    
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
            return sequence
    
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
            return sequence
    
    # Fallback: simple pattern for any remaining cases
    # Just use repeated pace 5 moves (inefficient but valid)
    for _ in range(target):
        sequence.append(5 * direction)
    sequence.append(0)
    return sequence

def solve_level3(input_text):
    """
    Solve Level 3 problem: generate sequence to reach target position within time limit
    
    Movement rules:
    - positive pace: move right 1 position, cost = pace
    - negative pace: move left 1 position, cost = abs(pace)  
    - pace = 0: stay put, cost = 1
    
    Key insight: We need to find the OPTIMAL sequence that minimizes total cost
    while reaching the target position within the time limit.
    
    Strategy: Use a mix of different pace values to minimize cost rather than 
    just repeating the same high-cost moves.
    """
    data = input_text.strip().split()
    if not data:
        return ""

    it = iter(data)
    try:
        n = int(next(it))
    except StopIteration:
        return ""

    outputs = []

    for _ in range(n):
        try:
            target_pos = int(next(it))
            time_limit = int(next(it))
        except StopIteration:
            break

        seq = find_optimal_sequence(target_pos, time_limit)
        
        # Validate the sequence
        valid, msg = validate_sequence(seq, target_pos, time_limit)
        if not valid:
            raise ValueError(f"Generated invalid sequence for pos={target_pos}: {msg}")
        
        outputs.append(" ".join(map(str, seq)))

    return "\n".join(outputs) + "\n"


def main():
    """Main function for stdin/stdout processing"""
    input_text = sys.stdin.read()
    output_text = solve_level3(input_text)
    sys.stdout.write(output_text)


def test_with_files():
    """Test function that processes .in files and generates .out files"""
    level3_dir = r"c:\\Users\\accou\\Code\\Coding_Contest\\CCC\\Challenge 2025\\Johannes\\LEVEL3\\level3"
    
    in_files = [f for f in os.listdir(level3_dir) if f.endswith('.in')]
    
    for in_file in in_files:
        print(f"Processing {in_file}...")
        
        in_path = os.path.join(level3_dir, in_file)
        with open(in_path, 'r') as f:
            input_text = f.read()
        
        output_text = solve_level3(input_text)
        
        out_file = in_file.replace('.in', '_generated.out')
        out_path = os.path.join(level3_dir, out_file)
        with open(out_path, 'w') as f:
            f.write(output_text)
        
        print(f"Generated {out_file}")
        
        # Compare with expected if exists
        expected_out_file = in_file.replace('.in', '.out')
        expected_out_path = os.path.join(level3_dir, expected_out_file)
        
        if os.path.exists(expected_out_path):
            with open(expected_out_path, 'r') as f:
                expected_output = f.read()
            
            # For this problem, we might have different valid solutions
            # So let's verify our solution works by checking if it reaches the target
            print(f"ℹ️  {in_file}: Verifying our solution...")
            
            # Parse our output and verify it works
            our_lines = output_text.strip().split('\n')
            expected_lines = expected_output.strip().split('\n')
            
            # Parse input to get targets
            with open(in_path, 'r') as f:
                input_lines = f.read().strip().split('\n')
            
            n = int(input_lines[0])
            for i in range(n):
                if i < len(our_lines) and i < len(input_lines) - 1:
                    target_pos, time_limit = map(int, input_lines[i + 1].split())
                    our_seq = list(map(int, our_lines[i].split()))
                    
                    # Simulate our sequence
                    pos = 0
                    time = 0
                    for pace in our_seq:
                        if pace > 0:
                            pos += 1
                            time += pace
                        elif pace < 0:
                            pos -= 1
                            time += abs(pace)
                        else:
                            time += 1
                    
                    if pos == target_pos and time <= time_limit:
                        print(f"✅ Sequence {i+1}: pos={pos}, time={time}, limit={time_limit}")
                    else:
                        print(f"❌ Sequence {i+1}: pos={pos} (target {target_pos}), time={time}, limit={time_limit}")
        else:
            print(f"ℹ️  {in_file}: No expected output file found")
        
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_with_files()
    else:
        main()