"""Test: What if X and Y are swapped in the file?"""

# What if these are actually swapped?
y_seq_maybe = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
x_seq_maybe = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

asteroid_x, asteroid_y = -3, 4

print("Test: X and Y SWAPPED")
print(f"Asteroid at ({asteroid_x}, {asteroid_y})\n")

x, y = 0, 0

for i in range(len(x_seq_maybe)):
    x_pace = x_seq_maybe[i]
    y_pace = y_seq_maybe[i]
    
    # Move based on pace
    if x_pace > 0:
        x += 1
    elif x_pace < 0:
        x -= 1
    
    if y_pace > 0:
        y += 1
    elif y_pace < 0:
        y -= 1
    
    dx = abs(x - asteroid_x)
    dy = abs(y - asteroid_y)
    collision = (dx <= 2 and dy <= 2)
    
    print(f"Step {i:2d}: pace=({x_pace:2d},{y_pace:2d}) → pos=({x:3d},{y:3d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")
    
    if i < 10 or collision:
        # Show more detail
        pass

print(f"\nFinal: ({x}, {y}), Target: (-6, 9)")
