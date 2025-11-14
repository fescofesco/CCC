"""
Comprehensive validator for Level 5 outputs.

Checks:
1. Velocity is 0 at start (both X and Y sequences start with 0)
2. Velocity is 0 at space station (both X and Y sequences end with 0)
3. Space station is reached (final position matches target)
4. Asteroid collision avoidance with proper safety radius
"""

def get_path_from_sequences(x_sequence, y_sequence):
    """
    Calculate the path taken by the spaceship over time.
    
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


def check_collision_radius_1(path, asteroid_x, asteroid_y):
    """
    Check collision with radius 1 around asteroid (3x3 grid).
    Asteroid at center, spaceship cannot enter any of the 8 surrounding squares.
    DEPRECATED - use radius 2 check instead.
    """
    forbidden_positions = set()
    for dx in range(-1, 2):  # -1, 0, 1
        for dy in range(-1, 2):  # -1, 0, 1
            forbidden_positions.add((asteroid_x + dx, asteroid_y + dy))
    
    collisions = []
    for i, (x, y) in enumerate(path):
        if (x, y) in forbidden_positions:
            collisions.append((i, x, y))
    
    return collisions


def check_collision_radius_2(path, asteroid_x, asteroid_y):
    """
    Check collision with radius 2 around asteroid (5x5 grid).
    Spaceship cannot enter within 2 squares (Chebyshev distance) of asteroid.
    """
    forbidden_positions = set()
    for dx in range(-2, 3):  # -2, -1, 0, 1, 2
        for dy in range(-2, 3):  # -2, -1, 0, 1, 2
            forbidden_positions.add((asteroid_x + dx, asteroid_y + dy))
    
    collisions = []
    for i, (x, y) in enumerate(path):
        if (x, y) in forbidden_positions:
            collisions.append((i, x, y))
    
    return collisions


def validate_case(x_seq, y_seq, target_x, target_y, asteroid_x, asteroid_y, case_num, use_radius_1=False):
    """Validate a single test case."""
    errors = []
    
    # Check 1: Start with velocity 0
    if x_seq[0] != 0:
        errors.append(f"X sequence does not start with 0 (starts with {x_seq[0]})")
    if y_seq[0] != 0:
        errors.append(f"Y sequence does not start with 0 (starts with {y_seq[0]})")
    
    # Check 2: End with velocity 0
    if x_seq[-1] != 0:
        errors.append(f"X sequence does not end with 0 (ends with {x_seq[-1]})")
    if y_seq[-1] != 0:
        errors.append(f"Y sequence does not end with 0 (ends with {y_seq[-1]})")
    
    # Check 3: Same length
    if len(x_seq) != len(y_seq):
        errors.append(f"Sequences have different lengths: X={len(x_seq)}, Y={len(y_seq)}")
        return errors, None, None
    
    # Check 4: Calculate path and verify target reached
    path = get_path_from_sequences(x_seq, y_seq)
    final_x, final_y = path[-1]
    
    if final_x != target_x:
        errors.append(f"Final X position {final_x} != target {target_x}")
    if final_y != target_y:
        errors.append(f"Final Y position {final_y} != target {target_y}")
    
    # Check 5: Collision detection
    if use_radius_1:
        collisions = check_collision_radius_1(path, asteroid_x, asteroid_y)
        radius_desc = "radius 1 (3x3 grid)"
    else:
        collisions = check_collision_radius_2(path, asteroid_x, asteroid_y)
        radius_desc = "radius 2 (5x5 grid)"
    
    if collisions:
        errors.append(f"COLLISION detected ({radius_desc}): {len(collisions)} collision(s)")
        errors.append(f"  First collision at step {collisions[0][0]}: position ({collisions[0][1]}, {collisions[0][2]})")
        if len(collisions) > 1:
            errors.append(f"  Last collision at step {collisions[-1][0]}: position ({collisions[-1][1]}, {collisions[-1][2]})")
    
    return errors, path, collisions


def validate_file(input_file, output_file, use_radius_1=False):
    """Validate an entire output file."""
    # Read input
    with open(input_file, 'r') as f:
        input_lines = f.readlines()
    
    # Read output
    with open(output_file, 'r') as f:
        output_lines = f.readlines()
    
    n = int(input_lines[0].strip())
    
    print(f"\nValidating: {input_file.name}")
    print(f"Using collision radius: {'1 (3x3 grid)' if use_radius_1 else '2 (5x5 grid)'}")
    print("=" * 70)
    
    total_errors = 0
    total_collisions = 0
    
    for i in range(n):
        # Parse input
        station_line = input_lines[1 + i * 2].strip()
        asteroid_line = input_lines[2 + i * 2].strip()
        
        pos_part, time_limit_str = station_line.split()
        target_x, target_y = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        asteroid_x, asteroid_y = map(int, asteroid_line.split(','))
        
        # Parse output (each case is 3 lines: X sequence, Y sequence, blank)
        x_seq_line = output_lines[i * 3].strip()
        y_seq_line = output_lines[i * 3 + 1].strip()
        
        if not x_seq_line or not y_seq_line:
            print(f"Case {i+1}: ERROR - Empty sequence")
            total_errors += 1
            continue
        
        x_seq = list(map(int, x_seq_line.split()))
        y_seq = list(map(int, y_seq_line.split()))
        
        # Validate
        errors, path, collisions = validate_case(
            x_seq, y_seq, target_x, target_y, asteroid_x, asteroid_y, i+1, use_radius_1
        )
        
        if errors:
            print(f"\nCase {i+1}: FAILED")
            print(f"  Target: ({target_x}, {target_y})")
            print(f"  Asteroid: ({asteroid_x}, {asteroid_y})")
            print(f"  Time limit: {time_limit}")
            for error in errors:
                print(f"  X {error}")
            total_errors += 1
            if collisions:
                total_collisions += 1
        else:
            # Only print every 100th success to avoid spam
            if (i + 1) % 100 == 0 or i < 5:
                final_pos = path[-1] if path else (None, None)
                print(f"Case {i+1}: OK - Reached {final_pos} in {len(x_seq)} steps")
    
    print("\n" + "=" * 70)
    if total_errors == 0:
        print(f"PASSED: ALL {n} CASES PASSED!")
    else:
        print(f"FAILED: {total_errors}/{n} cases FAILED")
        if total_collisions > 0:
            print(f"  {total_collisions} cases had collisions")
    
    return total_errors == 0


def main():
    from pathlib import Path
    
    base_path = Path(__file__).parent.parent.parent
    input_dir = base_path / "Input" / "level5"
    output_dir = base_path / "Felix" / "Outputs" / "level5"
    
    print("=" * 70)
    print("COMPREHENSIVE LEVEL 5 VALIDATOR")
    print("=" * 70)
    
    # Test files
    test_files = [
        ("level5_1_small.in", "level5_1_small.out"),
        ("level5_2_large.in", "level5_2_large.out"),
    ]
    
    print("\n" + "=" * 70)
    print("TESTING WITH RADIUS 2 (5x5 grid - current implementation)")
    print("=" * 70)
    
    all_passed_r2 = True
    for input_name, output_name in test_files:
        input_file = input_dir / input_name
        output_file = output_dir / output_name
        
        if not input_file.exists():
            print(f"\nSkipping {input_name} - file not found")
            continue
        if not output_file.exists():
            print(f"\nSkipping {output_name} - file not found")
            continue
        
        passed = validate_file(input_file, output_file, use_radius_1=False)
        all_passed_r2 = all_passed_r2 and passed
    
    print("\n" + "=" * 70)
    print("TESTING WITH RADIUS 1 (3x3 grid - alternative interpretation)")
    print("=" * 70)
    
    all_passed_r1 = True
    for input_name, output_name in test_files:
        input_file = input_dir / input_name
        output_file = output_dir / output_name
        
        if not input_file.exists() or not output_file.exists():
            continue
        
        passed = validate_file(input_file, output_file, use_radius_1=True)
        all_passed_r1 = all_passed_r1 and passed
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Radius 2 (5x5 grid): {'PASSED' if all_passed_r2 else 'FAILED'}")
    print(f"Radius 1 (3x3 grid): {'PASSED' if all_passed_r1 else 'FAILED'}")
    print()
    
    if all_passed_r2:
        print("PASSED: Current implementation (radius 2) is CORRECT!")
    elif all_passed_r1:
        print("WARNING: Need to switch to radius 1 (3x3 grid)")
    else:
        print("FAILED: Issues found in both interpretations")


if __name__ == "__main__":
    main()
