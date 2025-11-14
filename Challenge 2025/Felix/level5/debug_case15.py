"""Debug case 15 from level5_1_small.in"""

def get_path_from_sequences(x_sequence, y_sequence):
    """
    Calculate the path from pace sequences using time-based interpretation.
    Each pace represents a time period where position changes at START, then holds.
    X and Y move independently on their own timelines.
    """
    path = []
    x_pos, y_pos = 0, 0
    x_idx, y_idx = 0, 0
    x_elapsed, y_elapsed = 0, 0
    
    max_time = 1000  # Safety limit
    time = 0
    
    while time < max_time:
        # Record current position
        path.append((x_pos, y_pos))
        
        # Check if we're done (both sequences exhausted)
        if x_idx >= len(x_sequence) and y_idx >= len(y_sequence):
            break
        
        time += 1
        
        # Process X dimension
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            
            # At start of pace (elapsed==0), move the position
            if x_elapsed == 0 and x_pace != 0:
                x_pos += 1 if x_pace > 0 else -1
            
            x_elapsed += 1
            
            # Check if current pace is complete
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        # Process Y dimension
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            
            # At start of pace (elapsed==0), move the position
            if y_elapsed == 0 and y_pace != 0:
                y_pos += 1 if y_pace > 0 else -1
            
            y_elapsed += 1
            
            # Check if current pace is complete
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
    
    return path

# Case 15: Target (11,4), Asteroid (6,2), Time limit 122
x_sequence = [0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0]
y_sequence = [0, 5, 4, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]

target = (11, 4)
asteroid = (6, 2)

print("Case 15 Debug")
print(f"Target: {target}, Asteroid: {asteroid}")
print(f"X sequence: {x_sequence}")
print(f"Y sequence: {y_sequence}")
print()

path = get_path_from_sequences(x_sequence, y_sequence)

print(f"Path has {len(path)} positions")
print()

# Show path with time steps, highlighting step 21 and positions near asteroid
for i, (x, y) in enumerate(path):
    dx = abs(x - asteroid[0])
    dy = abs(y - asteroid[1])
    chebyshev = max(dx, dy)
    
    collision = (dx <= 2 and dy <= 2)
    
    marker = ""
    if i == 21:
        marker = " <<< STEP 21"
    if collision:
        marker += f" *** COLLISION (dx={dx}, dy={dy}, cheby={chebyshev})"
    
    print(f"Step {i:3d}: ({x:3d}, {y:3d}){marker}")
    
print()
print(f"Final position: {path[-1]}")
print(f"Target: {target}")
print(f"Reached target: {path[-1] == target}")
