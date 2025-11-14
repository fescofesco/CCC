import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from pathlib import Path


def get_path_from_sequences(x_sequence, y_sequence):
    """
    Calculate the actual path taken by the spaceship over time.
    
    Each pace costs time: |pace| if pace≠0, or 1 if pace=0.
    X and Y move SIMULTANEOUSLY - when both dimensions have non-zero pace at the same time,
    they both move in the SAME time step (diagonal movement allowed).
    
    Returns list of (x, y, time) tuples for each time step.
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
        path.append((x_pos, y_pos, t + 1))
    
    return path


def check_asteroid_collision(path, asteroid_x, asteroid_y):
    """
    Check if the path collides with the asteroid's safety zone.
    
    The asteroid has size 1 and the spaceship has size 1.
    Safety radius is 2, meaning the spaceship center cannot be within
    2 squares (Chebyshev distance) of the asteroid center.
    """
    forbidden_positions = set()
    
    # Calculate all forbidden positions (within Chebyshev distance 2)
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            forbidden_positions.add((asteroid_x + dx, asteroid_y + dy))
    
    collisions = []
    
    for x, y, time in path:
        if (x, y) in forbidden_positions:
            collisions.append((x, y, time))
    
    if collisions:
        return True, collisions
    
    return False, []


def validate_collision_for_file(input_file, output_file):
    """Validate collision avoidance for a single file."""
    # Read input
    with open(input_file, 'r') as f:
        input_lines = f.readlines()
    
    # Read output
    with open(output_file, 'r') as f:
        output_lines = f.readlines()
    
    n = int(input_lines[0].strip())
    
    collisions_found = []
    
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
            print(f"  Case {i+1}: ERROR - Empty sequence")
            collisions_found.append(f"Case {i+1}: Empty sequence")
            continue
        
        x_sequence = list(map(int, x_seq_line.split()))
        y_sequence = list(map(int, y_seq_line.split()))
        
        try:
            # Calculate path
            path = get_path_from_sequences(x_sequence, y_sequence)
            
            # Check collision
            has_collision, collision_points = check_asteroid_collision(path, asteroid_x, asteroid_y)
            
            if has_collision:
                print(f"  Case {i+1}: COLLISION DETECTED!")
                print(f"    Target: ({target_x},{target_y}), Asteroid: ({asteroid_x},{asteroid_y})")
                print(f"    Collision points: {collision_points[:5]}")  # Show first 5
                collisions_found.append(f"Case {i+1}: Collision at {collision_points[0]}")
            else:
                # Verify final position
                final_x, final_y, total_time = path[-1]
                if final_x != target_x or final_y != target_y:
                    print(f"  Case {i+1}: ERROR - Wrong final position ({final_x},{final_y}) != ({target_x},{target_y})")
                    collisions_found.append(f"Case {i+1}: Wrong position")
                elif total_time > time_limit:
                    print(f"  Case {i+1}: ERROR - Time limit exceeded {total_time} > {time_limit}")
                    collisions_found.append(f"Case {i+1}: Time limit exceeded")
                else:
                    print(f"  Case {i+1}: OK - No collision, reached ({final_x},{final_y}) in time {total_time}/{time_limit}")
        
        except Exception as e:
            print(f"  Case {i+1}: ERROR - {e}")
            collisions_found.append(f"Case {i+1}: {e}")
    
    return collisions_found


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
    
    print(f"Validating {len(input_files)} level 5 output files for asteroid collisions")
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
            collisions = validate_collision_for_file(input_file, output_file)
            
            if collisions:
                all_valid = False
                print(f"  FAILED: {len(collisions)} collision(s)")
            else:
                print(f"  PASSED: All cases valid")
        
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            all_valid = False
    
    print("\n" + "=" * 70)
    if all_valid:
        print("PASSED: All files passed asteroid collision validation!")
    else:
        print("FAILED: Some files have collisions or errors")


if __name__ == "__main__":
    main()
