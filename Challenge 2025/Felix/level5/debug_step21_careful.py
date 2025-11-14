"""Carefully debug step 21 - check if position is recorded before or after movement"""

def get_path_version1(x_sequence, y_sequence):
    """Version 1: Record position at START of each time step (BEFORE movement)"""
    path = []
    x_pos, y_pos = 0, 0
    x_idx, y_idx = 0, 0
    x_elapsed, y_elapsed = 0, 0
    
    max_time = 1000
    time = 0
    
    while time < max_time:
        # Record BEFORE movement
        path.append((x_pos, y_pos))
        
        if x_idx >= len(x_sequence) and y_idx >= len(y_sequence):
            break
        
        time += 1
        
        # Then move
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

def get_path_version2(x_sequence, y_sequence):
    """Version 2: Move first, THEN record position"""
    path = [(0, 0)]  # Start at origin
    x_pos, y_pos = 0, 0
    x_idx, y_idx = 0, 0
    x_elapsed, y_elapsed = 0, 0
    
    max_time = 1000
    time = 0
    
    while time < max_time:
        if x_idx >= len(x_sequence) and y_idx >= len(y_sequence):
            break
        
        time += 1
        
        # Move first
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
        
        # Then record
        path.append((x_pos, y_pos))
    
    return path

# Case 15
x_sequence = [0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0]
y_sequence = [0, 5, 4, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]

asteroid = (6, 2)

print("Version 1: Record position BEFORE movement each step")
path1 = get_path_version1(x_sequence, y_sequence)
print(f"Step 21: {path1[21]}")
print()

print("Version 2: Move FIRST, then record position")
path2 = get_path_version2(x_sequence, y_sequence)
print(f"Step 21: {path2[21]}")
print()

print("Which one gives (4,4) at step 21?")
if path1[21] == (4, 4):
    print("Version 1 gives (4,4)")
elif path2[21] == (4, 4):
    print("Version 2 gives (4,4)")
else:
    print(f"Neither! V1={path1[21]}, V2={path2[21]}")

print()
print("Let me trace manually:")
print("Time  X_pace  X_elapsed  X_pos  |  Y_pace  Y_elapsed  Y_pos")
x_pos, y_pos = 0, 0
x_idx, y_idx = 0, 0
x_elapsed, y_elapsed = 0, 0

for step in range(22):
    if step == 0:
        print(f"{step:4d}    -         -      {x_pos:2d}   |    -         -      {y_pos:2d}   START")
        continue
    
    # Get current paces
    x_pace = x_sequence[x_idx] if x_idx < len(x_sequence) else 0
    y_pace = y_sequence[y_idx] if y_idx < len(y_sequence) else 0
    
    # Move at start of pace
    if x_elapsed == 0 and x_pace != 0:
        x_pos += 1 if x_pace > 0 else -1
    if y_elapsed == 0 and y_pace != 0:
        y_pos += 1 if y_pace > 0 else -1
    
    print(f"{step:4d}  {x_pace:3d}       {x_elapsed:2d}      {x_pos:2d}   |  {y_pace:3d}       {y_elapsed:2d}      {y_pos:2d}")
    
    # Increment elapsed
    x_elapsed += 1
    y_elapsed += 1
    
    # Check if pace complete
    x_duration = abs(x_pace) if x_pace != 0 else 1
    y_duration = abs(y_pace) if y_pace != 0 else 1
    
    if x_elapsed >= x_duration:
        x_idx += 1
        x_elapsed = 0
    if y_elapsed >= y_duration:
        y_idx += 1
        y_elapsed = 0
