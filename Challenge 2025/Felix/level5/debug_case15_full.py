"""Debug case 15 with correct path logic"""

def get_path_from_sequences(x_sequence, y_sequence):
    """Corrected - no diagonals"""
    path = [(0, 0)]
    
    x_idx = 0
    x_pos = 0
    x_elapsed = 0
    
    y_idx = 0
    y_pos = 0
    y_elapsed = 0
    
    while x_idx < len(x_sequence) or y_idx < len(y_sequence):
        x_needs_move = False
        y_needs_move = False
        
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            if x_elapsed == 0 and x_pace != 0:
                x_needs_move = True
        
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            if y_elapsed == 0 and y_pace != 0:
                y_needs_move = True
        
        if x_needs_move and y_needs_move:
            x_pos += 1 if x_sequence[x_idx] > 0 else -1
            path.append((x_pos, y_pos))
            y_pos += 1 if y_sequence[y_idx] > 0 else -1
            path.append((x_pos, y_pos))
        elif x_needs_move:
            x_pos += 1 if x_sequence[x_idx] > 0 else -1
            path.append((x_pos, y_pos))
        elif y_needs_move:
            y_pos += 1 if y_sequence[y_idx] > 0 else -1
            path.append((x_pos, y_pos))
        else:
            path.append((x_pos, y_pos))
        
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
    
    return path

# Read case 15 from output
with open('c:/Users/felix/CCC/CCC/Challenge 2025/Felix/Outputs/level5/level5_1_small.out') as f:
    lines = [l.strip() for l in f.readlines()]
    x_seq_str = lines[30]
    y_seq_str = lines[31]
    x_seq = list(map(int, x_seq_str.split()))
    y_seq = list(map(int, y_seq_str.split()))

# Read case 15 from input
with open('c:/Users/felix/CCC/CCC/Challenge 2025/Input/level5/level5_1_small.in') as f:
    lines = [l.strip() for l in f.readlines()]
    # Line 0: 20
    # Line 1-2: case 1
    # ...
    # Line 29-30: case 15
    target_line = lines[29].split()
    target_x, target_y = map(int, target_line[0].split(','))
    asteroid_line = lines[30].split(',')
    asteroid_x = int(asteroid_line[0])
    asteroid_y = int(asteroid_line[1])

target = (target_x, target_y)
asteroid = (asteroid_x, asteroid_y)

print(f"Case 15: Target {target}, Asteroid {asteroid}")
print()

path = get_path_from_sequences(x_seq, y_seq)

print(f"Path length: {len(path)}")
print(f"Final position: {path[-1]}")
print(f"Target: {target}")
print(f"Match: {path[-1] == target}")
print()

# Check collisions
collisions = []
for i, (x, y) in enumerate(path):
    dx = abs(x - asteroid[0])
    dy = abs(y - asteroid[1])
    if dx <= 2 and dy <= 2:
        collisions.append((i, x, y, dx, dy))

if collisions:
    print(f"COLLISIONS FOUND: {len(collisions)}")
    for idx, x, y, dx, dy in collisions[:10]:
        print(f"  Step {idx}: ({x},{y}) - dx={dx}, dy={dy}")
else:
    print("NO COLLISIONS")
