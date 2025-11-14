"""Test: What if we DON'T count the initial pace=0?"""

x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

x, y = 0, 0
asteroid_x, asteroid_y = -3, 4

print("INTERPRETATION: Path includes starting position, then positions AFTER each pace")
print(f"Asteroid at ({asteroid_x}, {asteroid_y})\n")

# Path starts at origin
path = [(x, y)]
print(f"Path[0] = ({x}, {y}) - starting position")

for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    # Apply pace
    if x_pace > 0:
        x += 1
    elif x_pace < 0:
        x -= 1
    
    if y_pace > 0:
        y += 1
    elif y_pace < 0:
        y -= 1
    
    path.append((x, y))
    print(f"Path[{i+1}] after pace[{i}]=({x_pace:2d},{y_pace:2d}) → ({x:3d},{y:3d})")

print(f"\nTotal path length: {len(path)} positions (start + {len(x_seq)} paces)")
print(f"\nAt path index 15: {path[15]}")
print(f"At path index 16: {path[16]}")
