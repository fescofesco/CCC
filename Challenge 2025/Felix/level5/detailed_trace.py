"""Detailed trace with proper indexing."""

x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

print(f"Total paces: X={len(x_seq)}, Y={len(y_seq)}")
print(f"\nX sequence: {' '.join(map(str, x_seq))}")
print(f"Y sequence: {' '.join(map(str, y_seq))}")
print()

x, y = 0, 0
asteroid_x, asteroid_y = -3, 4

print(f"Asteroid at ({asteroid_x}, {asteroid_y})")
print(f"Starting position: ({x}, {y})")
print()

# The sequences represent the paces/velocities
# At each time step, we apply the pace
for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    # Apply the pace - move 1 unit in the direction of pace
    if x_pace > 0:
        x += 1
    elif x_pace < 0:
        x -= 1
    # if pace == 0, position doesn't change
    
    if y_pace > 0:
        y += 1
    elif y_pace < 0:
        y -= 1
    
    dx = abs(x - asteroid_x)
    dy = abs(y - asteroid_y)
    
    # Check collision
    collision = (dx <= 2 and dy <= 2)
    
    print(f"Index {i:2d}: pace=({x_pace:2d},{y_pace:2d}) → pos=({x:3d},{y:3d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")
    
    if collision:
        print(f"  *** FORBIDDEN at index {i}!")
