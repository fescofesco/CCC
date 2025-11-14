"""Test if sequential movement changes final position"""

def calculate_position_simple(sequence):
    """Simple: each pace moves position once"""
    position = 0
    for pace in sequence:
        if pace > 0:
            position += 1
        elif pace < 0:
            position -= 1
    return position

def get_final_position_sequential(x_seq, y_seq):
    """Sequential: X and Y move separately"""
    path = [(0, 0)]
    
    x_idx = 0
    x_pos = 0
    x_elapsed = 0
    
    y_idx = 0
    y_pos = 0
    y_elapsed = 0
    
    while x_idx < len(x_seq) or y_idx < len(y_seq):
        x_needs_move = False
        y_needs_move = False
        
        if x_idx < len(x_seq):
            x_pace = x_seq[x_idx]
            if x_elapsed == 0 and x_pace != 0:
                x_needs_move = True
        
        if y_idx < len(y_seq):
            y_pace = y_seq[y_idx]
            if y_elapsed == 0 and y_pace != 0:
                y_needs_move = True
        
        if x_needs_move and y_needs_move:
            x_pos += 1 if x_seq[x_idx] > 0 else -1
            path.append((x_pos, y_pos))
            y_pos += 1 if y_seq[y_idx] > 0 else -1
            path.append((x_pos, y_pos))
        elif x_needs_move:
            x_pos += 1 if x_seq[x_idx] > 0 else -1
            path.append((x_pos, y_pos))
        elif y_needs_move:
            y_pos += 1 if y_seq[y_idx] > 0 else -1
            path.append((x_pos, y_pos))
        else:
            path.append((x_pos, y_pos))
        
        if x_idx < len(x_seq):
            x_pace = x_seq[x_idx]
            pace_duration = abs(x_pace) if x_pace != 0 else 1
            x_elapsed += 1
            if x_elapsed >= pace_duration:
                x_idx += 1
                x_elapsed = 0
        
        if y_idx < len(y_seq):
            y_pace = y_seq[y_idx]
            pace_duration = abs(y_pace) if y_pace != 0 else 1
            y_elapsed += 1
            if y_elapsed >= pace_duration:
                y_idx += 1
                y_elapsed = 0
    
    return path[-1]

# Test case 15
x_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 0, 0]
y_seq = [0, 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, 0, 0]

x_simple = calculate_position_simple(x_seq)
y_simple = calculate_position_simple(y_seq)

final_sequential = get_final_position_sequential(x_seq, y_seq)

print(f"X sequence independent: {x_simple}")
print(f"Y sequence independent: {y_simple}")
print(f"Expected combined: ({x_simple}, {y_simple})")
print(f"Actual sequential: {final_sequential}")
print()

if (x_simple, y_simple) == final_sequential:
    print("✓ SAME - Sequential doesn't change final position!")
else:
    print(f"✗ DIFFERENT - Sequential changes final position!")
    print(f"  Difference: X={final_sequential[0]-x_simple}, Y={final_sequential[1]-y_simple}")
