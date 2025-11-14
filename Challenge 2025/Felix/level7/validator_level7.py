"""
Official Validator for Level 7 - Extracted from visualizer_lvl7.html
Validates spaceship movement with MULTIPLE asteroids.
"""

import sys
from pathlib import Path


# Constants from visualizer
MIN_PACE = 5
MAX_PACE = 1
AREA_COLLISION = 2


def get_valid_paces(pace):
    """
    Get valid next paces from current pace.
    Extracted from getValidPaces() in visualizer.
    """
    if pace == -MIN_PACE:
        return [pace + 1, pace, 0]
    elif pace == -MAX_PACE:
        return [pace, pace - 1]
    elif pace == 0:
        return [-MIN_PACE, pace, MIN_PACE]
    elif pace == MAX_PACE:
        return [pace + 1, pace]
    elif pace == MIN_PACE:
        return [0, pace, pace - 1]
    else:
        return [pace + 1, pace, pace - 1]


def validate_pace_sequence(paces, dimension_name):
    """
    Validate a pace sequence according to the rules.
    Returns (is_valid, error_message).
    """
    if not paces:
        return False, f"{dimension_name}: Empty pace sequence"
    
    # Rule: Must start with 0
    if paces[0] != 0:
        return False, f"{dimension_name}: Must start with pace 0, got {paces[0]}"
    
    # Rule: Must end with 0
    if paces[-1] != 0:
        return False, f"{dimension_name}: Must end with pace 0, got {paces[-1]}"
    
    # Rule: Each pace transition must be valid
    for i in range(len(paces) - 1):
        current_pace = paces[i]
        next_pace = paces[i + 1]
        valid_next = get_valid_paces(current_pace)
        
        if next_pace not in valid_next:
            return False, (f"{dimension_name}: Invalid transition from pace {current_pace} to {next_pace} "
                          f"at position {i}. Valid next paces: {valid_next}")
    
    # Rule: Paces must be in valid range
    for i, pace in enumerate(paces):
        if abs(pace) > MIN_PACE:
            return False, f"{dimension_name}: Pace {pace} at position {i} exceeds maximum (±{MIN_PACE})"
        if pace != 0 and abs(pace) < MAX_PACE:
            return False, f"{dimension_name}: Non-zero pace {pace} at position {i} is below minimum (±{MAX_PACE})"
    
    return True, f"{dimension_name}: Valid"


def expand_paces(paces):
    """
    Expand paces according to visualizer logic.
    Each pace is repeated |pace| times (minimum 1).
    
    Example: [0, 5, -3, 0] -> [0, 5,5,5,5,5, -3,-3,-3, 0]
    
    From visualizer: expandPaces(paces) { return paces.flatMap(pace => Array(Math.max(1, Math.abs(pace))).fill(pace)); }
    """
    expanded = []
    for pace in paces:
        repeat_count = max(1, abs(pace))
        expanded.extend([pace] * repeat_count)
    return expanded


def calculate_time(paces):
    """Calculate total time from pace sequence."""
    return sum(max(1, abs(pace)) for pace in paces)


def simulate_movement(x_paces, y_paces):
    """
    Simulate spaceship movement according to Entity.move() logic.
    Returns list of (x, y) positions at each step.
    
    From visualizer Entity.move():
    - Movement happens when ticks reaches |pace|
    - Position changes by sign(pace)
    - X and Y move independently based on their own pace values
    """
    # Expand paces
    x_paces_expanded = expand_paces(x_paces)
    y_paces_expanded = expand_paces(y_paces)
    
    # Determine simulation length
    sim_length = max(len(x_paces_expanded), len(y_paces_expanded))
    
    history = []
    x_pos, y_pos = 0, 0
    x_ticks, y_ticks = 0, 0
    x_idx, y_idx = 0, 0
    
    # Initial position at step 0
    history.append((x_pos, y_pos))
    
    for step in range(sim_length):
        # Get current paces (use last pace if we've run out)
        x_pace = x_paces_expanded[min(x_idx, len(x_paces_expanded) - 1)] if x_idx < len(x_paces_expanded) else 0
        y_pace = y_paces_expanded[min(y_idx, len(y_paces_expanded) - 1)] if y_idx < len(y_paces_expanded) else 0
        
        # Move X dimension (from Entity.move() logic)
        if abs(x_pace) > 0 and abs(x_pace) <= MIN_PACE:
            x_ticks += 1
            if x_ticks >= abs(x_pace):
                x_ticks = 0
                x_pos += 1 if x_pace > 0 else -1
        
        # Move Y dimension (from Entity.move() logic)
        if abs(y_pace) > 0 and abs(y_pace) <= MIN_PACE:
            y_ticks += 1
            if y_ticks >= abs(y_pace):
                y_ticks = 0
                y_pos += 1 if y_pace > 0 else -1
        
        # Advance to next pace in expanded sequences
        x_idx += 1
        y_idx += 1
        
        # Record position after movement
        history.append((x_pos, y_pos))
    
    return history


def check_asteroid_collisions(history, asteroids):
    """
    Check if path collides with ANY asteroid.
    
    From visualizer hasShipCollided():
    for (const asteroid of state.game.asteroids) {
      const d = state.game.ship.p.sub(asteroid.p);
      if (Math.abs(d.x) <= AREA_COLLISION && Math.abs(d.y) <= AREA_COLLISION) {
        return true;
      }
    }
    
    Returns (has_collision, step, ship_pos, asteroid_pos) or (False, -1, None, None)
    """
    for step, (ship_x, ship_y) in enumerate(history):
        for asteroid_x, asteroid_y in asteroids:
            dx = abs(ship_x - asteroid_x)
            dy = abs(ship_y - asteroid_y)
            
            # Collision if BOTH dx <= 2 AND dy <= 2
            if dx <= AREA_COLLISION and dy <= AREA_COLLISION:
                return True, step, (ship_x, ship_y), (asteroid_x, asteroid_y)
    
    return False, -1, None, None


def validate_solution(x_paces, y_paces, goal_x, goal_y, time_limit, asteroids):
    """
    Validate a complete solution.
    Returns (is_valid, message).
    """
    # Validate pace sequences
    valid_x, msg_x = validate_pace_sequence(x_paces, "X")
    if not valid_x:
        return False, msg_x
    
    valid_y, msg_y = validate_pace_sequence(y_paces, "Y")
    if not valid_y:
        return False, msg_y
    
    # Calculate time
    x_time = calculate_time(x_paces)
    y_time = calculate_time(y_paces)
    total_time = max(x_time, y_time)
    
    if total_time > time_limit:
        return False, f"Time limit exceeded: {total_time} > {time_limit}"
    
    # Simulate movement
    history = simulate_movement(x_paces, y_paces)
    
    # Check final position
    final_x, final_y = history[-1]
    if final_x != goal_x or final_y != goal_y:
        return False, f"Did not reach goal: final position ({final_x},{final_y}) != goal ({goal_x},{goal_y})"
    
    # Check asteroid collisions
    has_collision, collision_step, ship_pos, asteroid_pos = check_asteroid_collisions(history, asteroids)
    if has_collision:
        return False, (f"Collision at step {collision_step}: ship at {ship_pos} "
                      f"too close to asteroid at {asteroid_pos}")
    
    return True, f"Valid! Reached ({final_x},{final_y}) in {total_time}/{time_limit} steps"


def parse_input_file(input_path):
    """
    Parse level 7 input file.
    Format:
    N                    # Number of cases
    goal_x,goal_y limit  # Goal position and time limit
    A                    # Number of asteroids
    ax1,ay1 ax2,ay2 ... # Asteroids on one line, space-separated
    """
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    n = int(lines[0])
    cases = []
    
    idx = 1
    for case_num in range(n):
        # Parse goal and time limit
        goal_line = lines[idx]
        idx += 1
        
        parts = goal_line.split()
        goal_pos = parts[0]
        goal_x, goal_y = map(int, goal_pos.split(','))
        time_limit = int(parts[1])
        
        # Parse asteroid count
        asteroid_count = int(lines[idx])
        idx += 1
        
        # Parse asteroids (all on one line, space-separated)
        asteroids = []
        if asteroid_count > 0:
            asteroid_line = lines[idx]
            idx += 1
            
            asteroid_parts = asteroid_line.split()
            for asteroid_str in asteroid_parts:
                ax, ay = map(int, asteroid_str.split(','))
                asteroids.append((ax, ay))
        
        cases.append({
            'goal_x': goal_x,
            'goal_y': goal_y,
            'time_limit': time_limit,
            'asteroids': asteroids
        })
    
    return cases


def parse_output_file(output_path):
    """
    Parse level 7 output file.
    Format for each case:
    x_pace_sequence
    y_pace_sequence
    (blank line)
    """
    with open(output_path, 'r') as f:
        lines = f.readlines()
    
    solutions = []
    idx = 0
    
    while idx < len(lines):
        # Skip empty lines
        if not lines[idx].strip():
            idx += 1
            continue
        
        # Read X paces
        x_line = lines[idx].strip()
        idx += 1
        
        # Read Y paces
        if idx >= len(lines):
            break
        y_line = lines[idx].strip()
        idx += 1
        
        # Parse paces
        x_paces = list(map(int, x_line.split()))
        y_paces = list(map(int, y_line.split()))
        
        solutions.append({
            'x_paces': x_paces,
            'y_paces': y_paces
        })
    
    return solutions


def validate_output_file(input_path, output_path):
    """
    Validate an entire output file against its input.
    Returns (num_valid, num_total, results).
    """
    print("=" * 80)
    print("OFFICIAL VALIDATOR RESULTS (Level 7 - Multiple Asteroids)")
    print("=" * 80)
    print()
    
    # Parse files
    cases = parse_input_file(input_path)
    solutions = parse_output_file(output_path)
    
    if len(cases) != len(solutions):
        print(f"❌ ERROR: Number of cases mismatch!")
        print(f"   Input has {len(cases)} cases, output has {len(solutions)} solutions")
        return 0, len(cases), []
    
    results = []
    num_valid = 0
    
    for i, (case, solution) in enumerate(zip(cases, solutions), 1):
        is_valid, message = validate_solution(
            solution['x_paces'],
            solution['y_paces'],
            case['goal_x'],
            case['goal_y'],
            case['time_limit'],
            case['asteroids']
        )
        
        results.append((is_valid, message))
        
        if is_valid:
            num_valid += 1
            print(f"Case {i}: ✅ SUCCESS")
            print(f"  {message}")
            print(f"  goal: ({case['goal_x']},{case['goal_y']})")
            print(f"  asteroids: {len(case['asteroids'])} asteroids")
        else:
            print(f"Case {i}: ❌ FAILURE")
            print(f"  {message}")
            print(f"  goal: ({case['goal_x']},{case['goal_y']})")
            print(f"  time_limit: {case['time_limit']}")
            print(f"  asteroids: {case['asteroids']}")
        print()
    
    print("=" * 80)
    if num_valid == len(cases):
        print(f"ALL CASES VALID ✅")
    else:
        print(f"VALIDATION FAILED: {num_valid}/{len(cases)} cases valid ❌")
    print("=" * 80)
    
    return num_valid, len(cases), results


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validator_level7.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    if not Path(output_file).exists():
        print(f"Error: Output file not found: {output_file}")
        sys.exit(1)
    
    num_valid, num_total, results = validate_output_file(input_file, output_file)
    
    if num_valid < num_total:
        sys.exit(1)
