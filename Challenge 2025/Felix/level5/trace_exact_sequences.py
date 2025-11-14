"""Trace the exact sequences from the output file"""

def get_path_simultaneous(x_sequence, y_sequence):
    """Simultaneous movement - diagonal allowed"""
    x_time = sum(abs(p) if p != 0 else 1 for p in x_sequence)
    y_time = sum(abs(p) if p != 0 else 1 for p in y_sequence)
    max_time = max(x_time, y_time)
    
    path = []
    
    x_idx = 0
    x_pos = 0
    x_elapsed = 0
    
    y_idx = 0
    y_pos = 0
    y_elapsed = 0
    
    for t in range(max_time):
        # Move X if at start of pace
        if x_idx < len(x_sequence):
            x_pace = x_sequence[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            
            if x_elapsed == 0 and x_pace != 0:
                x_pos += 1 if x_pace > 0 else -1
            
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        # Move Y if at start of pace
        if y_idx < len(y_sequence):
            y_pace = y_sequence[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            
            if y_elapsed == 0 and y_pace != 0:
                y_pos += 1 if y_pace > 0 else -1
            
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
        
        path.append((x_pos, y_pos))
    
    return path

# The EXACT sequences from output file line 43-44 (case 15?)
x_seq = [0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0]
y_seq = [0, 5, 4, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]

path = get_path_simultaneous(x_seq, y_seq)

print(f"Total path length: {len(path)}")
print(f"\nPositions around step 21:")
for i in range(18, min(26, len(path))):
    pos = path[i]
    marker = " <<< INDEX 21" if i == 21 else ""
    if pos == (4, 4):
        marker += " <<< (4,4) FOUND!"
    print(f"  Index {i}: {pos}{marker}")

print(f"\nSearching for (4,4) in entire path:")
for i, pos in enumerate(path):
    if pos == (4, 4):
        print(f"  Found at index {i}: {pos}")

print(f"\nFinal position: {path[-1]}")
