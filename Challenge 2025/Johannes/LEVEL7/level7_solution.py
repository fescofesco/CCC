import heapq
import os
import sys
from collections import deque

def chebyshev_distance(x1, y1, x2, y2):
    """Calculate Chebyshev distance (max of absolute differences)."""
    return max(abs(x1 - x2), abs(y1 - y2))

def _axis_range(start, velocity, time_limit):
    """Return inclusive min/max reachable values for one axis within time_limit."""
    if velocity == 0:
        return start, start
    steps = time_limit // abs(velocity)
    displacement = steps if velocity > 0 else -steps
    end = start + displacement
    return (start, end) if start <= end else (end, start)

def filter_relevant_asteroids(asteroids, target_x, target_y, time_limit, detour_margin=20, safety_margin=2):
    """Drop asteroids that can never come near the playable area within time_limit.

    We consider the axis-aligned rectangle covering the entire path from origin
    to (target_x, target_y) plus some buffer for detours and the collision radius.
    Asteroids whose projected movement ranges never overlap that rectangle can be
    ignored safely because they will never threaten the ship.
    """
    min_x = min(0, target_x) - detour_margin - safety_margin
    max_x = max(0, target_x) + detour_margin + safety_margin
    min_y = min(0, target_y) - detour_margin - safety_margin
    max_y = max(0, target_y) + detour_margin + safety_margin

    relevant = []
    for asteroid in asteroids:
        ax_min, ax_max = _axis_range(asteroid['px'], asteroid['vx'], time_limit)
        ay_min, ay_max = _axis_range(asteroid['py'], asteroid['vy'], time_limit)

        if ax_max + safety_margin < min_x or ax_min - safety_margin > max_x:
            continue
        if ay_max + safety_margin < min_y or ay_min - safety_margin > max_y:
            continue

        relevant.append(asteroid)

    return relevant

def is_forbidden_cell_at_time(x, y, asteroids, time_step):
    """Check if position (x,y) collides with any asteroid at the given time step.
    
    Asteroids can be stationary or moving:
    - Stationary: {'px': x, 'py': y, 'vx': 0, 'vy': 0}
    - Moving: {'px': x, 'py': y, 'vx': vx, 'vy': vy}
    
    At time step t, asteroid position is (px + t*vx/|vx|, py + t*vy/|vy|) if vx!=0, vy!=0
    """
    for asteroid in asteroids:
        # Calculate asteroid position at this time step
        if asteroid['vx'] == 0:
            ax = asteroid['px']
        else:
            ax = asteroid['px'] + (time_step // abs(asteroid['vx']))
            
        if asteroid['vy'] == 0:
            ay = asteroid['py']
        else:
            ay = asteroid['py'] + (time_step // abs(asteroid['vy']))
        
        # Check collision (Chebyshev distance <= 2)
        if chebyshev_distance(x, y, ax, ay) <= 2:
            return True
    
    return False

def generate_sequence_1d(target, time_limit):
    """Generate a 1D pace sequence to reach target position."""
    if target == 0:
        return [0]
    
    direction = 1 if target > 0 else -1
    distance = abs(target)
    sequence = [0]
    
    if distance == 1:
        sequence.extend([5 * direction, 0])
    elif distance == 2:
        sequence.extend([5 * direction, 5 * direction, 0])
    elif distance >= 9:
        # Use pace 1 for efficiency
        extra_at_1 = distance - 9
        for pace in range(5, 0, -1):
            sequence.append(pace * direction)
        for _ in range(extra_at_1):
            sequence.append(1 * direction)
        for pace in range(2, 6):
            sequence.append(pace * direction)
        sequence.append(0)
    else:
        # Use valley patterns for 3-8
        patterns = {
            3: [5, 4, 5],
            4: [5, 4, 4, 5],
            5: [5, 4, 3, 4, 5],
            6: [5, 4, 3, 3, 4, 5],
            7: [5, 4, 3, 2, 3, 4, 5],
            8: [5, 4, 3, 2, 2, 3, 4, 5]
        }
        sequence.extend([p * direction for p in patterns[distance]])
        sequence.append(0)
    
    return sequence


def build_sequence_with_delays(base_seq, delays):
    """Insert zero-paces before each entry according to the provided delays."""
    if len(delays) != len(base_seq) + 1:
        raise ValueError("Delay vector must be one longer than the base sequence")

    seq = []
    for zeros, pace in zip(delays[:-1], base_seq):
        if zeros:
            seq.extend([0] * zeros)
        seq.append(pace)

    if delays[-1]:
        seq.extend([0] * delays[-1])

    return seq


def search_with_adaptive_waits(
    x_base,
    y_base,
    asteroids,
    time_limit,
    max_extra_wait=400,
    max_states=5000,
):
    """Resolve collisions by inserting waits (0-paces) before specific steps.

    We explore the space of sequences formed by the base pace lists plus
    inserted waits via a best-first search that prioritises schedules with
    fewer additional waits. When a collision happens, we create new candidates
    by delaying the next pending pace on the X or Y axis.
    """

    initial_x_delays = tuple(0 for _ in range(len(x_base) + 1))
    initial_y_delays = tuple(0 for _ in range(len(y_base) + 1))

    heap = [(0, initial_x_delays, initial_y_delays)]
    visited = set()
    expansions = 0

    while heap and expansions < max_states:
        wait_used, x_delays, y_delays = heapq.heappop(heap)
        state_key = (x_delays, y_delays)
        if state_key in visited:
            continue
        visited.add(state_key)
        expansions += 1

        x_seq = build_sequence_with_delays(x_base, x_delays)
        y_seq = build_sequence_with_delays(y_base, y_delays)
        success, info = simulate_sequences_with_time(x_seq, y_seq, asteroids, time_limit)

        if success:
            return x_seq, y_seq

        if wait_used >= max_extra_wait:
            continue

        # If we already ran out of time, adding more waits cannot help.
        if info.get("reason", "").startswith("Time limit"):
            continue

        for axis_key, base_seq, delays in (
            ("x", x_base, x_delays),
            ("y", y_base, y_delays),
        ):
            idx = info.get(f"{axis_key}_idx", len(base_seq))
            if idx >= len(base_seq):
                continue

            new_delays_list = list(delays)
            new_delays_list[idx] += 1
            new_wait = wait_used + 1
            if new_wait > max_extra_wait:
                continue

            if axis_key == "x":
                new_state = (tuple(new_delays_list), y_delays)
            else:
                new_state = (x_delays, tuple(new_delays_list))

            if new_state in visited:
                continue

            heapq.heappush(heap, (new_wait, new_state[0], new_state[1]))

    raise ValueError("Could not resolve collisions with adaptive waiting strategy")

def simulate_sequences_with_time(x_seq, y_seq, asteroids, time_limit, capture_path=False):
    """Simulate the sequences and check for collisions at each time step.

    Returns (success, info) where info contains metadata about the run. When
    capture_path is True, the full (x, y, time) path is included.
    """
    positions = [] if capture_path else None
    x, y = 0, 0
    x_idx, y_idx = 0, 0
    x_elapsed, y_elapsed = 0, 0
    time_step = 0

    if capture_path:
        positions.append((x, y, time_step))

    while (x_idx < len(x_seq) or y_idx < len(y_seq)) and time_step < time_limit:
        x_moved = False
        y_moved = False

        # Process X axis
        if x_idx < len(x_seq):
            x_pace = x_seq[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1

            if x_elapsed == 0 and x_pace != 0:
                x += 1 if x_pace > 0 else -1
                x_moved = True

            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0

        # Process Y axis
        if y_idx < len(y_seq):
            y_pace = y_seq[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1

            if y_elapsed == 0 and y_pace != 0:
                y += 1 if y_pace > 0 else -1
                y_moved = True

            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0

        time_step += 1
        if capture_path:
            positions.append((x, y, time_step))

        if is_forbidden_cell_at_time(x, y, asteroids, time_step):
            info = {
                "reason": f"Collision at ({x},{y}) at time {time_step}",
                "time": time_step,
                "x": x,
                "y": y,
                "x_idx": x_idx,
                "y_idx": y_idx,
                "x_elapsed": x_elapsed,
                "y_elapsed": y_elapsed,
                "x_moved": x_moved,
                "y_moved": y_moved,
            }
            if capture_path:
                info["path"] = positions
            return False, info

    if x_idx < len(x_seq) or y_idx < len(y_seq):
        fail_info = {
            "reason": "Time limit reached before completing sequences",
            "time": time_step,
            "x": x,
            "y": y,
            "x_idx": x_idx,
            "y_idx": y_idx,
            "x_elapsed": x_elapsed,
            "y_elapsed": y_elapsed,
        }
        if capture_path:
            fail_info["path"] = positions
        return False, fail_info

    success_info = {
        "reason": "Completed without collision",
        "time": time_step,
        "x": x,
        "y": y,
        "x_idx": x_idx,
        "y_idx": y_idx,
        "x_elapsed": x_elapsed,
        "y_elapsed": y_elapsed,
    }
    if capture_path:
        success_info["path"] = positions
    return True, success_info

DISABLE_ASTEROID_FILTER = os.environ.get("LEVEL7_DISABLE_ASTEROID_FILTER") == "1"


def find_collision_free_sequences(target_x, target_y, asteroids, time_limit):
    """Find collision-free sequences by trying different delay and detour strategies."""
    # Generate base sequences for each axis
    x_base = generate_sequence_1d(target_x, time_limit)
    y_base = generate_sequence_1d(target_y, time_limit)

    if DISABLE_ASTEROID_FILTER:
        relevant_asteroids = asteroids
    else:
        relevant_asteroids = filter_relevant_asteroids(asteroids, target_x, target_y, time_limit)
        if len(relevant_asteroids) < len(asteroids):
            print(
                f"Pruned asteroids: kept {len(relevant_asteroids)} of {len(asteroids)}",
                file=sys.stderr,
            )
    
    # Try different delay strategies
    strategies = []
    
    # Strategy 1: No delay (simultaneous movement)
    strategies.append((x_base, y_base, "No delay"))
    
    # Strategy 2: Y first, then X (delay X start)
    for delay in range(1, min(200, time_limit)):
        x_delayed = [0] * delay + x_base
        strategies.append((x_delayed, y_base, f"Delay X by {delay}"))
    
    # Strategy 3: X first, then Y (delay Y start)
    for delay in range(1, min(200, time_limit)):
        y_delayed = [0] * delay + y_base
        strategies.append((x_base, y_delayed, f"Delay Y by {delay}"))
    
    # Strategy 4: Detour - go in opposite Y direction first, then X, then target Y
    # This is useful when asteroids block the direct path
    for detour_dist in range(1, min(10, time_limit // 10)):
        # Go down/up first (opposite of target Y direction)
        detour_direction = -1 if target_y >= 0 else 1
        y_detour_first = generate_sequence_1d(detour_dist * detour_direction, time_limit)
        # Then reach final Y target
        y_detour_second = generate_sequence_1d(target_y - detour_dist * detour_direction, time_limit)
        # Combine Y sequences (remove the ending 0 from first, and starting 0 from second)
        y_detour = y_detour_first[:-1] + y_detour_second
        
        # Try with different X delays
        for x_delay in range(0, min(50, time_limit)):
            x_delayed = [0] * x_delay + x_base
            strategies.append((x_delayed, y_detour, f"Y detour {detour_dist}, X delay {x_delay}"))
    
    # Strategy 5: Detour - go in opposite X direction first, then target X, then Y  
    for detour_dist in range(1, min(10, time_limit // 10)):
        detour_direction = -1 if target_x >= 0 else 1
        x_detour_first = generate_sequence_1d(detour_dist * detour_direction, time_limit)
        x_detour_second = generate_sequence_1d(target_x - detour_dist * detour_direction, time_limit)
        x_detour = x_detour_first[:-1] + x_detour_second
        
        for y_delay in range(0, min(50, time_limit)):
            y_delayed = [0] * y_delay + y_base
            strategies.append((x_detour, y_delayed, f"X detour {detour_dist}, Y delay {y_delay}"))
    
    # Try each strategy
    for x_seq, y_seq, desc in strategies:
        # Check time limit
        x_time = sum(abs(p) if p != 0 else 1 for p in x_seq)
        y_time = sum(abs(p) if p != 0 else 1 for p in y_seq)
        if x_time > time_limit or y_time > time_limit:
            continue
        
        # Check final position
        x_pos = sum(1 if p > 0 else (-1 if p < 0 else 0) for p in x_seq)
        y_pos = sum(1 if p > 0 else (-1 if p < 0 else 0) for p in y_seq)
        if x_pos != target_x or y_pos != target_y:
            continue
        
        # Check collision using time-based simulation
        success, info = simulate_sequences_with_time(
            x_seq,
            y_seq,
            relevant_asteroids,
            time_limit,
        )
        
        if success:
            print(f"Found solution using: {desc}", file=sys.stderr)
            return x_seq, y_seq
    
    # Adaptive wait insertion fallback
    print("Falling back to adaptive wait search", file=sys.stderr)
    x_seq, y_seq = search_with_adaptive_waits(
        x_base,
        y_base,
        relevant_asteroids,
        time_limit,
        max_extra_wait=min(800, time_limit // 2),
        max_states=20000,
    )
    print("Adaptive wait search succeeded", file=sys.stderr)
    return x_seq, y_seq

def solve_level7(input_text):
    """Solve Level 7: Navigate to goal while avoiding moving asteroids."""
    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
    
    n = int(lines[0])
    idx = 1
    results = []

    for case_num in range(n):
        # Parse goal position and time limit
        goal_line = lines[idx].strip()
        pos_part, time_limit_str = goal_line.split()
        target_x, target_y = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        idx += 1
        
        # Parse asteroids
        asteroid_count_line = lines[idx].strip()
        idx += 1
        
        # Check if it's a count or asteroid data
        if ',' in asteroid_count_line:
            # It's asteroid data, count is 1
            asteroid_line = asteroid_count_line
            asteroid_count = len(asteroid_line.split())
        else:
            # It's a count
            asteroid_count = int(asteroid_count_line)
            asteroid_line = lines[idx].strip()
            idx += 1
        
        # Parse asteroid positions and velocities
        asteroids = []
        asteroid_data = asteroid_line.split()
        
        for ast_str in asteroid_data:
            parts = list(map(int, ast_str.split(',')))
            if len(parts) == 2:
                # Stationary asteroid
                px, py = parts
                asteroids.append({'px': px, 'py': py, 'vx': 0, 'vy': 0})
            elif len(parts) == 4:
                # Moving asteroid
                px, py, vx, vy = parts
                asteroids.append({'px': px, 'py': py, 'vx': vx, 'vy': vy})
            else:
                raise ValueError(f"Invalid asteroid format: {ast_str}")
        
        # Find collision-free sequences
        try:
            x_seq, y_seq = find_collision_free_sequences(target_x, target_y, asteroids, time_limit)
        except ValueError as e:
            print(f"ERROR in case {case_num + 1}: {e}", file=sys.stderr)
            # Fallback to simple sequences
            x_seq = generate_sequence_1d(target_x, time_limit)
            y_seq = generate_sequence_1d(target_y, time_limit)
        
        # Format output
        results.append(' '.join(map(str, x_seq)))
        results.append(' '.join(map(str, y_seq)))
        if case_num < n - 1:
            results.append('')  # Blank line between cases

    return '\n'.join(results) + '\n'

def main():
    """Read from stdin and write solution to stdout."""
    input_text = sys.stdin.read()
    output_text = solve_level7(input_text)
    sys.stdout.write(output_text)

if __name__ == "__main__":
    main()
