"""Test CORRECTED path calculation that prevents diagonal moves"""

def get_path_CORRECTED(x_sequence, y_sequence):
    """NO DIAGONAL MOVES - X and Y movements are sequential"""
    path = [(0, 0)]  # Start at origin
    
    x_idx = 0
    x_pos = 0
    x_elapsed = 0
    
    y_idx = 0
    y_pos = 0
    y_elapsed = 0
    
    while x_idx < len(x_sequence) or y_idx < len(y_sequence):
        x_needs_move = False
        y_needs_move = False
        
        # Check if X needs to move
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            if x_elapsed == 0 and x_pace != 0:
                x_needs_move = True
        
        # Check if Y needs to move
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            if y_elapsed == 0 and y_pace != 0:
                y_needs_move = True
        
        # If both need to move, move X first, record, then move Y, record
        if x_needs_move and y_needs_move:
            # Move X first
            x_pos += 1 if x_sequence[x_idx] > 0 else -1
            path.append((x_pos, y_pos))
            
            # Then move Y
            y_pos += 1 if y_sequence[y_idx] > 0 else -1
            path.append((x_pos, y_pos))
            
        elif x_needs_move:
            # Only X moves
            x_pos += 1 if x_sequence[x_idx] > 0 else -1
            path.append((x_pos, y_pos))
            
        elif y_needs_move:
            # Only Y moves
            y_pos += 1 if y_sequence[y_idx] > 0 else -1
            path.append((x_pos, y_pos))
            
        else:
            # Neither moves, just time passing
            path.append((x_pos, y_pos))
        
        # Advance time for X
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        # Advance time for Y
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
    
    return path

# Case 15 - from output file
x_sequence = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 0, 0]
y_sequence = [0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]

target = (11, 4)
asteroid = (6, 2)

path = get_path_CORRECTED(x_sequence, y_sequence)

print("CORRECTED path calculation (no diagonals)")
print(f"Path has {len(path)} positions\n")

# Check for diagonal moves
print("Checking for diagonal moves:")
has_diagonal = False
for i in range(len(path) - 1):
    curr = path[i]
    next_pos = path[i+1]
    dx = abs(next_pos[0] - curr[0])
    dy = abs(next_pos[1] - curr[1])
    
    if dx > 0 and dy > 0:
        print(f"  Index {i}: {curr} -> {next_pos} (DIAGONAL!)")
        has_diagonal = True

if not has_diagonal:
    print("  ✓ NO DIAGONAL MOVES FOUND!")

print("\nShow path around steps 20-25:")
for i in range(18, min(28, len(path))):
    x, y = path[i]
    dx = abs(x - asteroid[0])
    dy = abs(y - asteroid[1])
    collision = (dx <= 2 and dy <= 2)
    marker = f" *** COLLISION (dx={dx}, dy={dy})" if collision else ""
    print(f"  Index {i}: ({x:2d}, {y:2d}){marker}")

print(f"\nFinal position: {path[-1]}, Target: {target}")
print(f"Reached: {path[-1] == target}")
