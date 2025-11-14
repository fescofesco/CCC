"""Test: What if position is BEFORE applying pace?"""

x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

x, y = 0, 0
asteroid_x, asteroid_y = -3, 4

print("INTERPRETATION: Position at step i is BEFORE applying pace[i]")
print(f"Asteroid at ({asteroid_x}, {asteroid_y})\n")

for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    dx = abs(x - asteroid_x)
    dy = abs(y - asteroid_y)
    collision = (dx <= 2 and dy <= 2)
    
    print(f"Step {i:2d}: pos=({x:3d},{y:3d}) BEFORE pace=({x_pace:2d},{y_pace:2d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")
    
    # NOW apply pace
    if x_pace > 0:
        x += 1
    elif x_pace < 0:
        x -= 1
    
    if y_pace > 0:
        y += 1
    elif y_pace < 0:
        y -= 1

print(f"\nFinal position after all paces: ({x}, {y})")
print(f"Target: (-6, 9)")
