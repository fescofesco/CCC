import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from pathlib import Path


class DataLevelLoader:
    def __init__(self, level: int, base_path=None):
        """Initialize the DataLevelLoader for a specific level."""
        self.level = level
        if base_path is None:
            # Default to Challenge 2025 directory
            self.base_path = Path(__file__).parent.parent.parent
        else:
            self.base_path = Path(base_path)
        self.input_dir = self.base_path / "Input" / f"level{level}"
        self.output_dir = self.base_path / "Felix" / "Outputs" / f"level{level}"
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_input_files(self):
        """Load and return all .in files from the input directory."""
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")
        
        input_files = list(self.input_dir.glob("*.in"))
        if not input_files:
            raise FileNotFoundError(f"No .in files found in {self.input_dir}")
        
        return sorted(input_files)
    
    def get_output_dir(self):
        """Return the output directory path."""
        return self.output_dir


def calculate_position_and_time(sequence):
    """Calculate position and time using level2 logic."""
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
    
    return position, total_time


def generate_sequence(target_position, time_limit):
    """Generate a pace sequence to reach target_position within time_limit."""
    
    if target_position == 0:
        return [0]
    
    direction = 1 if target_position > 0 else -1
    target = abs(target_position)
    
    sequence = [0]
    
    # Special cases for very small targets
    if target == 1:
        sequence.extend([5 * direction, 0])
        return sequence
    elif target == 2:
        sequence.extend([5 * direction, 5 * direction, 0])
        return sequence
    
    # For targets >= 9, use pace 1 (fastest, minimal time cost)
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
    
    # For smaller targets (3-8), use symmetric valley pattern
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
    
    # Should not reach here
    raise ValueError(f"Cannot generate sequence for position {target_position}")


def simulate_movement(x_paces, y_paces):
    """
    Simulate movement based on pace sequences.
    Returns list of (x, y) positions at each step.
    
    From visualizer.html expandPaces logic:
    - Each pace value is repeated |pace| times (minimum 1 for pace=0)
    - Position changes happen at the START of each expanded pace
    """
    def expand_paces(paces):
        """Expand paces: each repeated max(1, |pace|) times"""
        expanded = []
        for pace in paces:
            repeat_count = max(1, abs(pace))
            for _ in range(repeat_count):
                expanded.append(pace)
        return expanded
    
    x_expanded = expand_paces(x_paces)
    y_expanded = expand_paces(y_paces)
    
    # Pad to same length
    max_len = max(len(x_expanded), len(y_expanded))
    x_expanded.extend([0] * (max_len - len(x_expanded)))
    y_expanded.extend([0] * (max_len - len(y_expanded)))
    
    history = []
    x_pos, y_pos = 0, 0
    
    for x_pace, y_pace in zip(x_expanded, y_expanded):
        # Move happens at START of pace (before recording position)
        if x_pace > 0:
            x_pos += 1
        elif x_pace < 0:
            x_pos -= 1
        
        if y_pace > 0:
            y_pos += 1
        elif y_pace < 0:
            y_pos -= 1
        
        history.append((x_pos, y_pos))
    
    return history


def check_asteroids_collision(history, asteroids):
    """
    Check if path collides with ANY asteroid's safety zone.
    
    From visualizer.html hasShipCollided():
    - Loops through all asteroids
    - Collision if BOTH dx <= 2 AND dy <= 2 for any asteroid
    
    Returns: (collision, step, position, asteroid) or (False, -1, None, None)
    """
    for step, (x, y) in enumerate(history):
        for asteroid_x, asteroid_y in asteroids:
            dx = abs(x - asteroid_x)
            dy = abs(y - asteroid_y)
            
            if dx <= 2 and dy <= 2:
                return True, step, (x, y), (asteroid_x, asteroid_y)
    
    return False, -1, None, None


def pad_sequences_to_avoid_asteroids(x_seq, y_seq, asteroids, target_x, target_y, time_limit):
    """
    Two-phase path-finding:
    1. Find grid path using A* that avoids asteroids
    2. Convert path to valid pace sequences
    """
    from heapq import heappush, heappop
    
    AREA_COLLISION = 2
    
    # Pre-compute forbidden zones around asteroids
    forbidden_positions = set()
    for ax, ay in asteroids:
        for dx in range(-AREA_COLLISION, AREA_COLLISION + 1):
            for dy in range(-AREA_COLLISION, AREA_COLLISION + 1):
                forbidden_positions.add((ax + dx, ay + dy))
    
    def is_position_safe(x, y):
        """Check if a position is safe (not too close to asteroids)"""
        return (x, y) not in forbidden_positions
    
    def find_grid_path():
        """A* to find path through grid positions"""
        # Priority queue: (f_score, g_score, x, y, path)
        start = (0, 0)
        goal = (target_x, target_y)
        
        # f = g + h (h = manhattan distance to goal)
        h_start = abs(target_x) + abs(target_y)
        heap = [(h_start, 0, start[0], start[1], [start])]
        visited = {start: 0}
        
        max_iterations = 1000000  # Allow much more exploration
        iterations = 0
        
        while heap and iterations < max_iterations:
            iterations += 1
            f, g, x, y, path = heappop(heap)
            
            # Reached goal
            if (x, y) == goal:
                print(f"    Path found after {iterations} iterations")
                return path
            
            # More generous path length limit
            if g > time_limit * 5:
                continue
            
            # Try all 4 directions (and staying still for obstacles)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
                nx, ny = x + dx, y + dy
                
                # Check if safe
                if not is_position_safe(nx, ny):
                    continue
                
                new_g = g + 1
                
                # More lenient visited check - allow revisiting with similar cost
                if (nx, ny) in visited and visited[(nx, ny)] < new_g - 5:
                    continue
                
                visited[(nx, ny)] = new_g
                
                # Calculate heuristic
                h = abs(nx - target_x) + abs(ny - target_y)
                f = new_g + h
                
                new_path = path + [(nx, ny)]
                heappush(heap, (f, new_g, nx, ny, new_path))
        
        print(f"    No path found after {iterations} iterations")
        return None
    
    def path_to_paces(path):
        """Convert grid path to pace sequences"""
        if not path or len(path) < 2:
            return [0], [0]
        
        # Extract X and Y movements
        x_moves = []
        y_moves = []
        
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            x_moves.append(x2 - x1)  # -1, 0, or 1
            y_moves.append(y2 - y1)  # -1, 0, or 1
        
        # Convert moves to pace sequences
        def moves_to_paces(moves):
            """Convert sequence of -1, 0, 1 moves to valid paces"""
            paces = [0]  # Start with 0
            
            i = 0
            while i < len(moves):
                move = moves[i]
                
                if move == 0:
                    # Staying still - add a 0 pace
                    if paces[-1] == 0:
                        pass  # Already at 0
                    elif abs(paces[-1]) == 5:
                        paces.append(0)  # Can go from ±5 to 0
                    else:
                        # Need to ramp to ±5 first
                        direction = 1 if paces[-1] > 0 else -1
                        while abs(paces[-1]) < 5:
                            paces.append(paces[-1] + direction)
                        paces.append(0)
                    i += 1
                else:
                    # Moving - count consecutive moves in same direction
                    direction = move
                    count = 0
                    while i < len(moves) and moves[i] == direction:
                        count += 1
                        i += 1
                    
                    # Generate paces for 'count' moves in 'direction'
                    # Use pace 5 (fastest) as much as possible
                    if paces[-1] == 0:
                        # From 0, must go to ±5
                        paces.append(5 * direction)
                        count -= 1
                    
                    # Continue moving
                    while count > 0:
                        # Try to use pace 1 (fastest for covering distance)
                        if abs(paces[-1]) == 1 or (abs(paces[-1]) > 1 and abs(paces[-1]) <= 5):
                            # Can stay at current pace or adjust by ±1
                            if abs(paces[-1]) > 1:
                                paces.append(paces[-1] - direction)  # Decrease towards 1
                            else:
                                paces.append(paces[-1])  # Stay at 1
                        elif abs(paces[-1]) == 5:
                            paces.append(4 * direction)  # Ramp down
                        else:
                            paces.append(paces[-1])  # Continue
                        count -= 1
            
            # End with 0
            if paces[-1] != 0:
                # Ramp to 5 then to 0
                direction = 1 if paces[-1] > 0 else -1
                while abs(paces[-1]) < 5:
                    paces.append(paces[-1] + direction)
                paces.append(0)
            
            return paces
        
        x_paces = moves_to_paces(x_moves)
        y_paces = moves_to_paces(y_moves)
        
        return x_paces, y_paces
    
    # Phase 1: Find grid path using A*
    print(f"    Searching for grid path to ({target_x}, {target_y}) avoiding {len(asteroids)} asteroids...")
    grid_path = find_grid_path()
    
    if grid_path:
        print(f"    Found grid path with {len(grid_path)} steps")
        # Phase 2: Convert to paces
        x_paces, y_paces = path_to_paces(grid_path)
        
        # Pad to same length
        max_len = max(len(x_paces), len(y_paces))
        x_padded = x_paces + [0] * (max_len - len(x_paces))
        y_padded = y_paces + [0] * (max_len - len(y_paces))
        
        # Verify with validator
        from validator_level7 import simulate_movement, check_asteroid_collisions
        history = simulate_movement(x_padded, y_padded)
        collision, _, _, _ = check_asteroid_collisions(history, asteroids)
        
        if not collision:
            x_time = sum(max(1, abs(p)) for p in x_padded)
            y_time = sum(max(1, abs(p)) for p in y_padded)
            if max(x_time, y_time) <= time_limit:
                print(f"    Paces valid! Time: {max(x_time, y_time)}/{time_limit}")
                return x_padded, y_padded
            else:
                print(f"    Paces exceed time limit: {max(x_time, y_time)} > {time_limit}")
        else:
            print(f"    Converted paces have collision, trying fallback...")
    
    # If path finding failed, raise error
    raise ValueError(f"Cannot find collision-free path to ({target_x},{target_y}) avoiding {len(asteroids)} asteroids - grid search exhausted")


def solve_level7(input_file, output_file):
    """Solve a single level 7 input file."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    n = int(lines[0].strip())
    results = []
    
    line_idx = 1
    for i in range(n):
        # Parse station position and time limit
        station_line = lines[line_idx].strip()
        line_idx += 1
        
        pos_part, time_limit_str = station_line.split()
        target_x, target_y = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        
        # Parse number of asteroids
        num_asteroids_line = lines[line_idx].strip()
        line_idx += 1
        num_asteroids = int(num_asteroids_line)
        
        # Parse asteroids (all on one line, space-separated)
        asteroids_line = lines[line_idx].strip()
        line_idx += 1
        
        asteroids = []
        if asteroids_line:
            asteroid_strs = asteroids_line.split()
            for asteroid_str in asteroid_strs:
                ax, ay = map(int, asteroid_str.split(','))
                asteroids.append((ax, ay))
        
        # Generate base sequences
        x_sequence = generate_sequence(target_x, time_limit)
        y_sequence = generate_sequence(target_y, time_limit)
        
        # Pad and adjust to avoid all asteroids
        try:
            x_padded, y_padded = pad_sequences_to_avoid_asteroids(
                x_sequence, y_sequence, asteroids, target_x, target_y, time_limit
            )
            print(f"  Case {i+1}: Found collision-free path (avoiding {num_asteroids} asteroids)")
        except Exception as e:
            print(f"  Case {i+1} ERROR: {e}")
            # Use base sequences as fallback
            max_len = max(len(x_sequence), len(y_sequence))
            x_padded = x_sequence + [0] * (max_len - len(x_sequence))
            y_padded = y_sequence + [0] * (max_len - len(y_sequence))
        
        # Format output
        x_seq_str = ' '.join(map(str, x_padded))
        y_seq_str = ' '.join(map(str, y_padded))
        
        results.append(x_seq_str)
        results.append(y_seq_str)
        results.append('')  # Blank line between cases
    
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')


def main():
    """Main function to process all level 7 input files."""
    loader = DataLevelLoader(level=7)
    input_files = loader.load_input_files()
    output_dir = loader.get_output_dir()
    
    print(f"Processing {len(input_files)} input files for Level 7")
    
    for input_file in input_files:
        output_file = output_dir / input_file.name.replace('.in', '.out')
        print(f"Processing {input_file.name}...")
        try:
            solve_level7(input_file, output_file)
            print(f"  Output written to {output_file}")
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    print("Done!")


if __name__ == "__main__":
    main()
