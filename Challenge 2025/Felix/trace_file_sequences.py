"""
Trace the ACTUAL sequences from the output file level5_1_small.out
to see if position (4,4) appears at step index 21
"""

# ACTUAL sequences from level5_1_small.out line 30-32 (case 15)
X_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 0, 0]
Y_seq = [0, 5, 4, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -3, -2, -1, -1, -1, -1, -1, -1, 0, 0]

# Asteroid at (6, 2)
asteroid_x, asteroid_y = 6, 2

def trace_path(X_seq, Y_seq):
    """Trace path with SIMULTANEOUS X/Y movement (diagonals allowed)"""
    x, y = 0, 0
    time = 0
    path = [(x, y, time)]
    
    x_index = 0
    y_index = 0
    x_elapsed = 0
    y_elapsed = 0
    
    while x_index < len(X_seq) or y_index < len(Y_seq):
        # Determine what moves this time step
        x_moves = x_elapsed == 0 and x_index < len(X_seq)
        y_moves = y_elapsed == 0 and y_index < len(Y_seq)
        
        # Move X if needed
        if x_moves:
            x_pace = X_seq[x_index]
            if x_pace != 0:
                x += 1 if x_pace > 0 else -1
                x_elapsed = abs(x_pace)
            else:
                x_elapsed = 1
            x_index += 1
        
        # Move Y if needed
        if y_moves:
            y_pace = Y_seq[y_index]
            if y_pace != 0:
                y += 1 if y_pace > 0 else -1
                y_elapsed = abs(y_pace)
            else:
                y_elapsed = 1
            y_index += 1
        
        # Decrement elapsed times
        step_time = min(x_elapsed if x_elapsed > 0 else float('inf'),
                       y_elapsed if y_elapsed > 0 else float('inf'))
        
        if step_time == float('inf'):
            break
            
        x_elapsed -= step_time
        y_elapsed -= step_time
        time += step_time
        
        path.append((x, y, time))
    
    return path

path = trace_path(X_seq, Y_seq)

print("FILE SEQUENCES:")
print(f"X: {X_seq}")
print(f"Y: {Y_seq}")
print(f"Asteroid at: ({asteroid_x}, {asteroid_y})")
print()

# Show around step 21
print("Path around step index 21:")
for i in range(max(0, 18), min(len(path), 25)):
    x, y, t = path[i]
    dx = abs(x - asteroid_x)
    dy = abs(y - asteroid_y)
    collision = "COLLISION!" if dx <= 2 and dy <= 2 else ""
    marker = " <-- STEP 21" if i == 21 else ""
    print(f"  Index {i}: ({x}, {y}) at time {t} | dx={dx}, dy={dy} {collision}{marker}")

# Check if (4,4) appears anywhere
print("\nSearching for (4,4) in entire path:")
for i, (x, y, t) in enumerate(path):
    if x == 4 and y == 4:
        dx = abs(x - asteroid_x)
        dy = abs(y - asteroid_y)
        print(f"  Found (4,4) at index {i}, time {t} | dx={dx}, dy={dy} | COLLISION!")

print(f"\nFinal position: ({path[-1][0]}, {path[-1][1]})")
