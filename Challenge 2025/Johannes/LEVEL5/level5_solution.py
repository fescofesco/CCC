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

def build_sequences_from_path(path):
    """Convert a path of coordinates into X and Y pace sequences.
    
    NOTE: Sequences can have different lengths! When one ends, it implicitly
    continues with pace=0 (no movement) until the other finishes.
    """
    if len(path) <= 1:
        return [0], [0]
    
    # Split path into segments by axis changes
    segments = []
    i = 0
    
    while i < len(path) - 1:
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx = x2 - x1
        dy = y2 - y1
        
        if dx != 0:
            axis = 'x'
            direction = 1 if dx > 0 else -1
        elif dy != 0:
            axis = 'y'
            direction = 1 if dy > 0 else -1
        else:
            i += 1
            continue
        
        # Count consecutive moves in same direction on same axis
        count = 1
        j = i + 1
        while j < len(path) - 1:
            nx1, ny1 = path[j]
            nx2, ny2 = path[j + 1]
            ndx = nx2 - nx1
            ndy = ny2 - ny1
            
            if axis == 'x' and ndx * direction > 0 and ndy == 0:
                count += 1
                j += 1
            elif axis == 'y' and ndy * direction > 0 and ndx == 0:
                count += 1
                j += 1
            else:
                break
        
        segments.append({'axis': axis, 'direction': direction, 'count': count})
        i = j
    
    # Build sequences - each axis has its own independent sequence
    x_seq = [0]
    y_seq = [0]
    
    for segment in segments:
        move_seq = generate_efficient_move_sequence(segment['count'], segment['direction'])
        
        if segment['axis'] == 'x':
            x_seq.extend(move_seq)
            x_seq.append(0)
        else:
            y_seq.extend(move_seq)
            y_seq.append(0)
    
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

        # Find collision-free path and convert to sequences
        path = bfs_find_path(xs, ys, ax, ay)
        x_seq, y_seq = build_sequences_from_path(path)
        
        x_str = " ".join(map(str, x_seq))
        y_str = " ".join(map(str, y_seq))

        results.append(x_str)
        results.append(y_str)
        if case_num < n - 1:
            results.append("")

    return "\n".join(results) + "\n"

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
