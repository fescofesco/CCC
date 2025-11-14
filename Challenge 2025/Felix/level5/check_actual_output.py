"""Check case 15 with ACTUAL output sequences"""

def get_path_from_sequences(x_sequence, y_sequence):
    path = []
    x_pos, y_pos = 0, 0
    x_idx, y_idx = 0, 0
    x_elapsed, y_elapsed = 0, 0
    
    max_time = 1000
    time = 0
    
    while time < max_time:
        path.append((x_pos, y_pos))
        
        if x_idx >= len(x_sequence) and y_idx >= len(y_sequence):
            break
        
        time += 1
        
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            
            if x_elapsed == 0 and x_pace != 0:
                x_pos += 1 if x_pace > 0 else -1
            
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            
            if y_elapsed == 0 and y_pace != 0:
                y_pos += 1 if y_pace > 0 else -1
            
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
    
    return path

# ACTUAL sequences from output file (case 15, line 30-31)
x_sequence = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 0, 0]
y_sequence = [0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]

target = (11, 4)
asteroid = (6, 2)

path = get_path_from_sequences(x_sequence, y_sequence)

print(f"Case 15 with ACTUAL output sequences")
print(f"Target: {target}, Asteroid: {asteroid}")
print()

# Find (4,4) and the jump
for i in range(len(path)):
    if i >= 18 and i <= 25:
        x, y = path[i]
        dx = abs(x - asteroid[0])
        dy = abs(y - asteroid[1])
        collision = (dx <= 2 and dy <= 2)
        marker = ""
        if collision:
            marker = f" *** COLLISION dx={dx} dy={dy}"
        print(f"Index {i}: ({x}, {y}){marker}")

print("\nLooking for diagonal jump (4,4)->(5,5):")
for i in range(len(path)-1):
    curr = path[i]
    next_pos = path[i+1]
    dx = abs(next_pos[0] - curr[0])
    dy = abs(next_pos[1] - curr[1])
    
    if dx > 0 and dy > 0:  # Both changed = diagonal
        print(f"  Index {i}: {curr} -> {next_pos} (DIAGONAL! dx={dx}, dy={dy})")
