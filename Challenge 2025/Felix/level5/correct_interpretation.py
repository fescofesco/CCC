"""Correct interpretation: Both dimensions can move in the SAME time step."""

x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

asteroid_x, asteroid_y = -3, 4

print("FINAL INTERPRETATION:")
print("- Each pace entry costs TIME")
print("- During that time, we move ±1 in dimensions where pace ≠ 0")
print("- X and Y move INDEPENDENTLY based on their own pace sequences")
print("="*70)

# Track X and Y separately with their own time
x_pos = 0
y_pos = 0
x_time = 0
y_time = 0

# Build position at each time step
max_time = 0
for i in range(len(x_seq)):
    if x_seq[i] != 0:
        x_time += abs(x_seq[i])
    else:
        x_time += 1
        
    if y_seq[i] != 0:
        y_time += abs(y_seq[i])
    else:
        y_time += 1
    
    max_time = max(x_time, y_time)

# Now simulate second by second
x_positions = []
y_positions = []

x_idx = 0
x_pos = 0
x_elapsed = 0

y_idx = 0
y_pos = 0
y_elapsed = 0

for t in range(1, max_time + 1):
    # Update X position
    if x_idx < len(x_seq):
        x_pace = x_seq[x_idx]
        if x_pace == 0:
            pace_duration = 1
        else:
            pace_duration = abs(x_pace)
        
        if x_elapsed == 0:  # Start of this pace
            if x_pace > 0:
                x_pos += 1
            elif x_pace < 0:
                x_pos -= 1
        
        x_elapsed += 1
        if x_elapsed >= pace_duration:
            x_idx += 1
            x_elapsed = 0
    
    # Update Y position  
    if y_idx < len(y_seq):
        y_pace = y_seq[y_idx]
        if y_pace == 0:
            pace_duration = 1
        else:
            pace_duration = abs(y_pace)
        
        if y_elapsed == 0:  # Start of this pace
            if y_pace > 0:
                y_pos += 1
            elif y_pace < 0:
                y_pos -= 1
        
        y_elapsed += 1
        if y_elapsed >= pace_duration:
            y_idx += 1
            y_elapsed = 0
    
    dx = abs(x_pos - asteroid_x)
    dy = abs(y_pos - asteroid_y)
    collision = (dx <= 2 and dy <= 2)
    
    if t <= 45:
        print(f"Step {t:2d}: pos=({x_pos:3d},{y_pos:3d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")

print(f"\nFinal: ({x_pos}, {y_pos})")
