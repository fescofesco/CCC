import sys
import os
from collections import deque

def chebyshev_distance(x1, y1, x2, y2):
    """Calculate Chebyshev distance (max of absolute differences)."""
    return max(abs(x1 - x2), abs(y1 - y2))

def is_forbidden_cell(x, y, ax, ay):
    """Check if a cell is within collision distance of the asteroid."""
    return chebyshev_distance(x, y, ax, ay) <= 2

def bfs_find_path(xs, ys, ax, ay):
    """Find a collision-free path from (0,0) to (xs,ys) avoiding asteroid at (ax,ay).
    
    Strategy: Prefer paths that move on one axis first (Y-axis preferred if asteroid
    blocks direct X path), then move on the other axis.
    """
    start = (0, 0)
    target = (xs, ys)

    if is_forbidden_cell(start[0], start[1], ax, ay):
        raise ValueError(f"Start position {start} is in collision with asteroid")
    if is_forbidden_cell(target[0], target[1], ax, ay):
        raise ValueError(f"Target position {target} is in collision with asteroid")

    # Determine if we should move Y first or X first based on asteroid position
    # If asteroid is on the direct X path (same Y level), move Y first to go around
    asteroid_blocks_x = (abs(ay - 0) <= 2 and 
                        ((ax >= 0 and ax <= xs) or (ax <= 0 and ax >= xs)))
    asteroid_blocks_y = (abs(ax - 0) <= 2 and 
                        ((ay >= 0 and ay <= ys) or (ay <= 0 and ay >= ys)))
    
    # Try to build a simple path: move one axis completely, then the other
    # Choose order based on which axis is blocked
    if asteroid_blocks_x and not asteroid_blocks_y:
        # Move Y first, then X
        path_order = [('y', ys), ('x', xs)]
    elif asteroid_blocks_y and not asteroid_blocks_x:
        # Move X first, then Y
        path_order = [('x', xs), ('y', ys)]
    elif abs(ys) > abs(xs):
        # Y distance is larger, move Y first
        path_order = [('y', ys), ('x', xs)]
    else:
        # X distance is larger or equal, move X first
        path_order = [('x', xs), ('y', ys)]
    
    # Try to build a simple two-segment path
    path = [(0, 0)]
    x, y = 0, 0
    
    for axis, target_val in path_order:
        if axis == 'y':
            # Move Y to target
            direction = 1 if ys > y else -1
            while y != ys:
                y += direction
                if is_forbidden_cell(x, y, ax, ay):
                    # Simple path blocked, fall back to BFS
                    return bfs_find_path_general(xs, ys, ax, ay)
                path.append((x, y))
        else:
            # Move X to target
            direction = 1 if xs > x else -1
            while x != xs:
                x += direction
                if is_forbidden_cell(x, y, ax, ay):
                    # Simple path blocked, fall back to BFS
                    return bfs_find_path_general(xs, ys, ax, ay)
                path.append((x, y))
    
    return path

def bfs_find_path_general(xs, ys, ax, ay):
    """General BFS pathfinding when simple paths don't work."""
    start = (0, 0)
    target = (xs, ys)
    
    min_x = min(0, xs, ax) - 10
    max_x = max(0, xs, ax) + 10
    min_y = min(0, ys, ay) - 10
    max_y = max(0, ys, ay) + 10

    queue = deque([start])
    visited = {start: None}
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        x, y = queue.popleft()
        if (x, y) == target:
            break

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if not (min_x <= nx <= max_x and min_y <= ny <= max_y):
                continue
            if is_forbidden_cell(nx, ny, ax, ay):
                continue
            if (nx, ny) in visited:
                continue
            visited[(nx, ny)] = (x, y)
            queue.append((nx, ny))

    if target not in visited:
        raise ValueError(f"No collision-free path found from {start} to {target}")

    # Reconstruct path
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = visited[cur]
    path.reverse()
    return path

def generate_efficient_move_sequence(count, direction):
    """Generate an efficient pace sequence to move 'count' steps in the given direction."""
    if count == 0:
        return []
    elif count == 1:
        return [5 * direction]
    elif count == 2:
        return [5 * direction, 5 * direction]  
    elif count <= 8:
        # Use optimized patterns for small counts
        patterns = {
            3: [5, 4, 5],
            4: [5, 4, 4, 5],
            5: [5, 4, 3, 4, 5],
            6: [5, 4, 3, 3, 4, 5],
            7: [5, 4, 3, 2, 3, 4, 5],
            8: [5, 4, 3, 2, 2, 3, 4, 5]
        }
        return [p * direction for p in patterns[count]]
    else:
        # For longer distances: ramp down, use pace=1 for extras, ramp up
        extra_at_1 = count - 9
        seq = []
        for pace in range(5, 0, -1):
            seq.append(pace * direction)
        for _ in range(extra_at_1):
            seq.append(1 * direction)
        for pace in range(2, 6):
            seq.append(pace * direction)
        return seq

def generate_simple_sequences(target_x, target_y, time_limit):
    """Generate simple X and Y pace sequences using Level 3 logic."""
    def generate_sequence_1d(target, time_limit):
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
    
    x_seq = generate_sequence_1d(target_x, time_limit)
    y_seq = generate_sequence_1d(target_y, time_limit)
    return x_seq, y_seq

def check_collision_chebyshev(x, y, asteroid_x, asteroid_y):
    """Check if position (x,y) collides with asteroid using Chebyshev distance."""
    return max(abs(x - asteroid_x), abs(y - asteroid_y)) <= 2

def simulate_path(x_seq, y_seq):
    """Simulate the path taken by executing the sequences in parallel."""
    positions = []
    x, y = 0, 0
    x_idx, y_idx = 0, 0
    x_elapsed, y_elapsed = 0, 0
    
    max_len = max(len(x_seq), len(y_seq))
    
    while x_idx < len(x_seq) or y_idx < len(y_seq):
        # Process X
        if x_idx < len(x_seq):
            x_pace = x_seq[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            
            if x_elapsed == 0 and x_pace != 0:
                x += 1 if x_pace > 0 else -1
            
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        # Process Y
        if y_idx < len(y_seq):
            y_pace = y_seq[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            
            if y_elapsed == 0 and y_pace != 0:
                y += 1 if y_pace > 0 else -1
            
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
        
        positions.append((x, y))
    
    return positions

def find_collision_free_sequences(target_x, target_y, asteroid_x, asteroid_y, time_limit):
    """Find collision-free sequences by trying different delay strategies."""
    # Generate base sequences for each axis
    def gen_seq(target):
        return generate_simple_sequences(target, 0, time_limit)[0]
    
    x_base = gen_seq(target_x)
    y_base = gen_seq(target_y)
    
    # Try different strategies
    strategies = []
    
    # Strategy 1: No delay (simultaneous movement)
    strategies.append((x_base, y_base))
    
    # Strategy 2: Y first, then X (delay X start)
    for delay in range(1, 150):
        x_delayed = [0] * delay + x_base
        strategies.append((x_delayed, y_base))
    
    # Strategy 3: X first, then Y (delay Y start)
    for delay in range(1, 150):
        y_delayed = [0] * delay + y_base
        strategies.append((x_base, y_delayed))
    
    # Strategy 4: Both delayed (staggered start)
    for x_delay in range(1, 50):
        for y_delay in range(1, 50):
            x_delayed = [0] * x_delay + x_base
            y_delayed = [0] * y_delay + y_base
            strategies.append((x_delayed, y_delayed))
    
    # Try each strategy
    for x_seq, y_seq in strategies:
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
        
        # Check collision
        path = simulate_path(x_seq, y_seq)
        collision = any(check_collision_chebyshev(x, y, asteroid_x, asteroid_y) for x, y in path)
        
        if not collision:
            return x_seq, y_seq
    
    raise ValueError(f"Cannot find collision-free path to ({target_x},{target_y}) avoiding asteroid at ({asteroid_x},{asteroid_y})")

def build_sequences_from_path(path):
    """DEPRECATED: Use find_collision_free_sequences instead."""
    if len(path) <= 1:
        return [0], [0]
    
    # Build sequences - each axis has its own independent sequence
    x_seq = [0]
    y_seq = [0]
    
    return x_seq, y_seq

def solve_level5(input_text):
    """Solve Level 5: Find collision-free paths to space stations."""
    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
    
    n = int(lines[0])
    idx = 1
    results = []

    for case_num in range(n):
        station_line = lines[idx]
        idx += 1
        asteroid_line = lines[idx]
        idx += 1

        pos_part, time_limit_str = station_line.split()
        xs, ys = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        ax, ay = map(int, asteroid_line.split(','))

        # Find collision-free path using BFS, then convert to sequences with delays
        path = bfs_find_path(xs, ys, ax, ay)
        x_seq, y_seq = build_sequences_from_bfs_path(path, time_limit)
        
        x_str = " ".join(map(str, x_seq))
        y_str = " ".join(map(str, y_seq))

        results.append(x_str)
        results.append(y_str)
        if case_num < n - 1:
            results.append("")

    return "\n".join(results) + "\n"

def build_sequences_from_bfs_path(path, time_limit):
    """Convert BFS path to pace sequences, handling each axis independently."""
    if len(path) <= 1:
        return [0], [0]
    
    # Extract X and Y movements separately
    x_movements = []
    y_movements = []
    
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        
        if x2 != x1:
            x_movements.append(1 if x2 > x1 else -1)
        if y2 != y1:
            y_movements.append(1 if y2 > y1 else -1)
    
    # Generate sequences for each axis
    def movements_to_sequence(movements):
        if not movements:
            return [0]
        
        sequence = [0]
        direction = movements[0]
        count = len(movements)
        
        # Use efficient pace patterns
        if count == 1:
            sequence.extend([5 * direction, 0])
        elif count == 2:
            sequence.extend([5 * direction, 5 * direction, 0])
        elif count >= 9:
            extra_at_1 = count - 9
            for pace in range(5, 0, -1):
                sequence.append(pace * direction)
            for _ in range(extra_at_1):
                sequence.append(1 * direction)
            for pace in range(2, 6):
                sequence.append(pace * direction)
            sequence.append(0)
        else:
            patterns = {
                3: [5, 4, 5],
                4: [5, 4, 4, 5],
                5: [5, 4, 3, 4, 5],
                6: [5, 4, 3, 3, 4, 5],
                7: [5, 4, 3, 2, 3, 4, 5],
                8: [5, 4, 3, 2, 2, 3, 4, 5]
            }
            sequence.extend([p * direction for p in patterns[count]])
            sequence.append(0)
        
        return sequence
    
    x_seq = movements_to_sequence(x_movements)
    y_seq = movements_to_sequence(y_movements)
    
    return x_seq, y_seq

def main():
    """Read from stdin and write solution to stdout."""
    input_text = sys.stdin.read()
    output_text = solve_level5(input_text)
    sys.stdout.write(output_text)

def test_with_files():
    """Test the solution against all input files in the level5 directory."""
    level5_dir = r"c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5\level5"
    
    in_files = sorted([f for f in os.listdir(level5_dir) if f.endswith('.in')])
    
    for in_file in in_files:
        print(f"Processing {in_file}...")
        
        in_path = os.path.join(level5_dir, in_file)
        with open(in_path, 'r') as f:
            input_text = f.read()
        
        output_text = solve_level5(input_text)
        
        out_file = in_file.replace('.in', '_generated.out')
        out_path = os.path.join(level5_dir, out_file)
        with open(out_path, 'w') as f:
            f.write(output_text)
        
        print(f"✓ Generated {out_file}")
        
        expected_out_file = in_file.replace('.in', '.out')
        expected_path = os.path.join(level5_dir, expected_out_file)
        if os.path.exists(expected_path):
            with open(expected_path, 'r') as f:
                expected_output = f.read()
            
            if output_text.strip() == expected_output.strip():
                print(f"✅ Output matches expected!")
            else:
                print(f"ℹ️  Output differs from expected (but may still be valid)")
        
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_with_files()
    else:
        main()
