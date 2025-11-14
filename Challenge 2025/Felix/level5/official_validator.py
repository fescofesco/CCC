"""
Official validator extracted from visualizer.html
This matches the exact validation logic used by the official CCC visualizer.
"""

import sys
import os

# Constants from visualizer
MIN_PACE = 5
MAX_PACE = 1
AREA_COLLISION = 2


def get_valid_paces(pace):
    """
    Calculate all paces that can legally follow the given pace.
    Extracted from visualizer.html getValidPaces function.
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
    Validate a single pace sequence (X or Y).
    Returns (valid, error_message)
    
    From visualizer.html parseInputAndSolution logic.
    """
    if not paces:
        return False, f"{dimension_name}: Empty sequence"
    
    # Rule: First pace must be 0
    if paces[0] != 0:
        return False, f"{dimension_name}: The first pace must be 0 (got {paces[0]})"
    
    last_pace = 0
    for i, pace in enumerate(paces):
        abs_pace = abs(pace)
        
        # Rule: Pace must be 0 or in range [1, 5]
        if pace != 0 and (abs_pace < MAX_PACE or abs_pace > MIN_PACE):
            return False, f"{dimension_name}: Pace {pace} at index {i} is invalid! Must be 0 or ±1 to ±5"
        
        # Rule: Cannot change direction without 0 in between
        if last_pace != 0 and pace != 0:
            if (last_pace > 0 and pace < 0) or (last_pace < 0 and pace > 0):
                return False, f"{dimension_name}: Pace progression {last_pace} → {pace} at index {i} is invalid! Changing directions requires a pace of 0 in between."
        
        # Rule: Pace progression must be valid
        valid_next_paces = get_valid_paces(last_pace)
        if pace not in valid_next_paces:
            return False, f"{dimension_name}: Pace progression {last_pace} → {pace} at index {i} is invalid! Valid options: {valid_next_paces}"
        
        last_pace = pace
    
    # Rule: Last pace must be 0
    if last_pace != 0:
        return False, f"{dimension_name}: The last pace must be 0 (got {last_pace})"
    
    return True, "Valid"


def expand_paces(paces):
    """
    Expand the solution paces.
    From visualizer.html expandPaces function.
    
    Each pace value is repeated |pace| times (minimum 1).
    For example: [0, 5, -3, 0] → [0, 5, 5, 5, 5, 5, -3, -3, -3, 0]
    """
    expanded = []
    for pace in paces:
        count = max(1, abs(pace))
        expanded.extend([pace] * count)
    return expanded


def calculate_time(paces):
    """
    Calculate total time for a pace sequence.
    Time = sum of max(1, |pace|) for each pace
    """
    return sum(max(1, abs(pace)) for pace in paces)


def simulate_movement(x_paces, y_paces):
    """
    Simulate spaceship movement and return full history.
    From visualizer.html Entity.move() and calculateHistory logic.
    
    Returns:
        List of (x, y, step_index) tuples representing position at each step
    """
    # Expand paces (each pace value repeated |pace| times)
    x_expanded = expand_paces(x_paces)
    y_expanded = expand_paces(y_paces)
    
    # Pad to same length
    max_len = max(len(x_expanded), len(y_expanded))
    x_expanded.extend([0] * (max_len - len(x_expanded)))
    y_expanded.extend([0] * (max_len - len(y_expanded)))
    
    # Simulate movement
    x, y = 0, 0
    x_ticks, y_ticks = 0, 0
    history = [(x, y, 0)]  # Initial position
    
    for step in range(max_len):
        x_pace = x_expanded[step]
        y_pace = y_expanded[step]
        
        # Move X if pace is active
        if abs(x_pace) > 0 and abs(x_pace) <= MIN_PACE:
            x_ticks += 1
            if x_ticks >= abs(x_pace):
                x_ticks = 0
                x += 1 if x_pace > 0 else -1
        
        # Move Y if pace is active
        if abs(y_pace) > 0 and abs(y_pace) <= MIN_PACE:
            y_ticks += 1
            if y_ticks >= abs(y_pace):
                y_ticks = 0
                y += 1 if y_pace > 0 else -1
        
        history.append((x, y, step + 1))
    
    return history


def check_asteroid_collision(history, asteroid_x, asteroid_y):
    """
    Check if path collides with asteroid.
    From visualizer.html hasShipCollided function.
    
    Collision occurs when BOTH:
    - |ship_x - asteroid_x| <= AREA_COLLISION (2)
    - |ship_y - asteroid_y| <= AREA_COLLISION (2)
    
    Returns (has_collision, step_index, ship_x, ship_y) or (False, None, None, None)
    """
    for x, y, step in history:
        dx = abs(x - asteroid_x)
        dy = abs(y - asteroid_y)
        
        if dx <= AREA_COLLISION and dy <= AREA_COLLISION:
            return True, step, x, y
    
    return False, None, None, None


def validate_solution(x_paces, y_paces, goal_x, goal_y, time_limit, asteroids):
    """
    Complete validation using official visualizer logic.
    
    Args:
        x_paces: List of X dimension paces
        y_paces: List of Y dimension paces
        goal_x: Target X position
        goal_y: Target Y position
        time_limit: Maximum allowed time
        asteroids: List of (x, y) tuples
    
    Returns:
        (success, message, details_dict)
    """
    # Validate X pace sequence
    valid_x, msg_x = validate_pace_sequence(x_paces, "X")
    if not valid_x:
        return False, msg_x, {}
    
    # Validate Y pace sequence
    valid_y, msg_y = validate_pace_sequence(y_paces, "Y")
    if not valid_y:
        return False, msg_y, {}
    
    # Calculate time used
    x_time = calculate_time(x_paces)
    y_time = calculate_time(y_paces)
    
    # Pad sequences to same time length (from visualizer logic)
    if x_time > y_time:
        y_paces = y_paces + [0] * (x_time - y_time)
    elif y_time > x_time:
        x_paces = x_paces + [0] * (y_time - x_time)
    
    total_time = max(x_time, y_time)
    
    # Check time limit
    if total_time > time_limit:
        return False, f"Too many paces provided: {total_time} > {time_limit}", {
            'x_time': x_time,
            'y_time': y_time,
            'total_time': total_time,
            'time_limit': time_limit
        }
    
    # Simulate movement
    history = simulate_movement(x_paces, y_paces)
    
    # Check for collisions
    for asteroid_x, asteroid_y in asteroids:
        collision, step, ship_x, ship_y = check_asteroid_collision(history, asteroid_x, asteroid_y)
        if collision:
            return False, f"The spaceship collided at step: {step}/{len(history)-1}", {
                'collision_step': step,
                'ship_position': (ship_x, ship_y),
                'asteroid_position': (asteroid_x, asteroid_y),
                'distance': (abs(ship_x - asteroid_x), abs(ship_y - asteroid_y))
            }
    
    # Get final position and velocity
    final_x, final_y, final_step = history[-1]
    
    # Verify reached goal
    if final_x != goal_x or final_y != goal_y:
        return False, f"The spaceship did not reach the station: Ship Position ({final_x},{final_y}) ≠ Goal Position ({goal_x},{goal_y})", {
            'final_position': (final_x, final_y),
            'goal_position': (goal_x, goal_y),
            'difference': (final_x - goal_x, final_y - goal_y)
        }
    
    # Verify stopped at goal (velocity must be 0)
    # From visualizer: shipNotInPaceWithGoal = state.game.ship.v.x !== 0 || state.game.ship.v.y !== 0
    if x_paces[-1] != 0 or y_paces[-1] != 0:
        return False, f"The spaceship did not stop at the station: Final pace ({x_paces[-1]},{y_paces[-1]}) ≠ (0,0)", {
            'final_pace': (x_paces[-1], y_paces[-1])
        }
    
    return True, "The spaceship docked successfully with the station!", {
        'final_position': (final_x, final_y),
        'total_time': total_time,
        'time_limit': time_limit,
        'steps': len(history) - 1
    }


def validate_output_file(input_file, output_file):
    """
    Validate an entire output file against its input.
    
    Returns:
        (all_valid, results_list)
        where results_list is [(case_num, success, message, details), ...]
    """
    # Parse input file
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    n = int(lines[0])
    cases = []
    for i in range(n):
        station_line = lines[1 + i * 2]
        asteroid_line = lines[2 + i * 2]
        
        pos_part, time_limit_str = station_line.split()
        goal_x, goal_y = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        
        asteroid_x, asteroid_y = map(int, asteroid_line.split(','))
        
        cases.append({
            'goal': (goal_x, goal_y),
            'time_limit': time_limit,
            'asteroids': [(asteroid_x, asteroid_y)]
        })
    
    # Parse output file
    with open(output_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    results = []
    all_valid = True
    
    for i, case in enumerate(cases):
        x_paces = list(map(int, lines[i * 2].split()))
        y_paces = list(map(int, lines[i * 2 + 1].split()))
        
        success, message, details = validate_solution(
            x_paces, y_paces,
            case['goal'][0], case['goal'][1],
            case['time_limit'],
            case['asteroids']
        )
        
        results.append((i + 1, success, message, details))
        if not success:
            all_valid = False
    
    return all_valid, results


def main():
    """Test with case 15 from level5_1_small"""
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        
        all_valid, results = validate_output_file(input_file, output_file)
        
        print("=" * 80)
        print("OFFICIAL VALIDATOR RESULTS (from visualizer.html logic)")
        print("=" * 80)
        
        for case_num, success, message, details in results:
            status = "✅ SUCCESS" if success else "❌ FAILURE"
            print(f"\nCase {case_num}: {status}")
            print(f"  {message}")
            if details:
                for key, value in details.items():
                    print(f"  {key}: {value}")
        
        print("\n" + "=" * 80)
        if all_valid:
            print("ALL CASES VALID ✅")
        else:
            failed_count = sum(1 for _, success, _, _ in results if not success)
            print(f"VALIDATION FAILED: {failed_count}/{len(results)} cases have errors ❌")
        print("=" * 80)
        
        sys.exit(0 if all_valid else 1)
    
    else:
        # Test case 15 specifically
        print("Testing Case 15 from level5_1_small...")
        print()
        
        # Case 15: Target (11,4), Asteroid (6,2)
        x_paces = [0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0]
        y_paces = [0, 5, 4, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]
        
        success, message, details = validate_solution(
            x_paces, y_paces,
            goal_x=11, goal_y=4,
            time_limit=122,
            asteroids=[(6, 2)]
        )
        
        print("=" * 80)
        print("OFFICIAL VALIDATOR RESULT")
        print("=" * 80)
        print(f"Status: {'✅ SUCCESS' if success else '❌ FAILURE'}")
        print(f"Message: {message}")
        if details:
            print("\nDetails:")
            for key, value in details.items():
                print(f"  {key}: {value}")
        print("=" * 80)


if __name__ == "__main__":
    main()
