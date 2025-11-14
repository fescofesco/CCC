"""Check all positions from pace simulation - simple output."""

x_seq = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
y_seq = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

ax, ay = 3, 0
x_pos, y_pos = 0, 0

print("All positions visited:")
print(f"Start: ({x_pos},{y_pos})")

positions_visited = [(x_pos, y_pos)]

for i in range(max(len(x_seq), len(y_seq))):
    x_pace = x_seq[i] if i < len(x_seq) else 0
    y_pace = y_seq[i] if i < len(y_seq) else 0
    
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    positions_visited.append((x_pos, y_pos))
    dist = max(abs(x_pos - ax), abs(y_pos - ay))
    print(f"Step {i}: ({x_pos},{y_pos}) dist={dist}")

print(f"\nUnique positions: {set(positions_visited)}")

# Check for corner positions
if (1, 2) in positions_visited:
    print("ERROR: Position (1,2) was visited!")
if (5, 2) in positions_visited:
    print("ERROR: Position (5,2) was visited!")
