"""Find the jump from (4,4) to (5,5)"""

def get_path_from_sequences(x_sequence, y_sequence):
    """Current implementation"""
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

# Case 15
x_sequence = [0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0]
y_sequence = [0, 5, 4, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]

path = get_path_from_sequences(x_sequence, y_sequence)

print("Looking for (4,4) and what comes after:")
for i in range(len(path)):
    if path[i] == (4, 4):
        print(f"Found (4,4) at index {i}")
        # Show context
        for j in range(max(0, i-3), min(len(path), i+5)):
            marker = " <<< HERE" if j == i else ""
            if j == i+1:
                marker += " <<< NEXT STEP"
            print(f"  Index {j}: {path[j]}{marker}")
        print()

print("\nLooking for the (4,4) -> (5,5) jump:")
for i in range(len(path)-1):
    if path[i] == (4, 4) and path[i+1] == (5, 5):
        print(f"FOUND DIAGONAL JUMP at index {i} -> {i+1}")
        print(f"  {path[i]} -> {path[i+1]}")
