"""Quick collision check for level 5 outputs."""

def check_collision(path, asteroid_x, asteroid_y):
    """Check if path has any collision with asteroid safety zone."""
    for i, (x, y) in enumerate(path):
        dx = abs(x - asteroid_x)
        dy = abs(y - asteroid_y)
        if dx <= 2 and dy <= 2:
            return True, i, x, y, dx, dy
    return False, -1, -1, -1, -1, -1


def get_path_from_sequences(x_seq, y_seq):
    """Calculate path from sequences with correct time-based movement."""
    max_time = 0
    x_time = sum(abs(p) if p != 0 else 1 for p in x_seq)
    y_time = sum(abs(p) if p != 0 else 1 for p in y_seq)
    max_time = max(x_time, y_time)
    
    path = []
    
    x_idx = 0
    x_pos = 0
    x_elapsed = 0
    
    y_idx = 0
    y_pos = 0
    y_elapsed = 0
    
    for t in range(max_time):
        # Update X position
        if x_idx < len(x_seq):
            x_pace = x_seq[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            
            if x_elapsed == 0:
                if x_pace > 0:
                    x_pos += 1
                elif x_pace < 0:
                    x_pos -= 1
            
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        # Update Y position
        if y_idx < len(y_seq):
            y_pace = y_seq[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            
            if y_elapsed == 0:
                if y_pace > 0:
                    y_pos += 1
                elif y_pace < 0:
                    y_pos -= 1
            
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
        
        path.append((x_pos, y_pos))
    
    return path


def validate_file(input_file, output_file):
    """Validate one output file."""
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    with open(output_file, 'r') as f:
        output_lines = [line.strip() for line in f.readlines()]
    
    n = int(lines[0])
    print(f"\nValidating {output_file.split('\\')[-1]}: {n} cases")
    
    collisions_found = 0
    
    for i in range(n):
        # Parse input
        station_line = lines[1 + i * 2]
        asteroid_line = lines[2 + i * 2]
        
        pos_part, time_limit_str = station_line.split()
        target_x, target_y = map(int, pos_part.split(','))
        asteroid_x, asteroid_y = map(int, asteroid_line.split(','))
        
        # Parse output
        x_seq = list(map(int, output_lines[i * 3].split()))
        y_seq = list(map(int, output_lines[i * 3 + 1].split()))
        
        # Get path and check collision
        path = get_path_from_sequences(x_seq, y_seq)
        has_collision, step, x, y, dx, dy = check_collision(path, asteroid_x, asteroid_y)
        
        if has_collision:
            collisions_found += 1
            print(f"  Case {i+1}: COLLISION at step {step} - ship at ({x},{y}), asteroid at ({asteroid_x},{asteroid_y}), dx={dx}, dy={dy}")
    
    if collisions_found == 0:
        print(f"  ✓ ALL {n} CASES PASS - No collisions!")
    else:
        print(f"  ✗ {collisions_found}/{n} cases have collisions")
    
    return collisions_found == 0


if __name__ == "__main__":
    import sys
    sys.path.append('c:\\Users\\felix\\CCC\\CCC\\Challenge 2025')
    
    input_dir = 'c:\\Users\\felix\\CCC\\CCC\\Challenge 2025\\Input\\level5\\'
    output_dir = 'c:\\Users\\felix\\CCC\\CCC\\Challenge 2025\\Felix\\Outputs\\level5\\'
    
    files = [
        ('level5_1_small.in', 'level5_1_small.out'),
        ('level5_2_large.in', 'level5_2_large.out'),
    ]
    
    all_pass = True
    for inp, out in files:
        passed = validate_file(input_dir + inp, output_dir + out)
        all_pass = all_pass and passed
    
    print("\n" + "="*60)
    if all_pass:
        print("SUCCESS: All test cases pass collision checks!")
    else:
        print("FAILURE: Some test cases have collisions")
    print("="*60)
