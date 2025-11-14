"""Verify the user's path calculation."""

x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

asteroid_x, asteroid_y = -3, 4

print("User's expected path:")
expected_path = [
    (0,0), (-1,0), (-2,0), (-3,0), (-3,1), (-4,1), (-5,2), (-5,3),
    (-6,3), (-6,4), (-6,5), (-6,6), (-6,6), (-7,6), (-7,7), (-7,8),
    (-7,9), (-6,9)
]

for i, (x, y) in enumerate(expected_path):
    dx = abs(x - asteroid_x)
    dy = abs(y - asteroid_y)
    collision = (dx <= 2 and dy <= 2)
    print(f"Step {i:2d}: ({x:3d},{y:3d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")

print("\n" + "="*70)
print("My calculation (position AFTER applying pace):")
print("="*70)

x, y = 0, 0
path = []

for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    # Apply pace - move based on pace
    if x_pace > 0:
        x += 1
    elif x_pace < 0:
        x -= 1
    
    if y_pace > 0:
        y += 1
    elif y_pace < 0:
        y -= 1
    
    path.append((x, y))
    
    dx = abs(x - asteroid_x)
    dy = abs(y - asteroid_y)
    collision = (dx <= 2 and dy <= 2)
    
    print(f"Step {i:2d}: pace=({x_pace:2d},{y_pace:2d}) → ({x:3d},{y:3d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")

print("\n" + "="*70)
print("COMPARISON:")
print("="*70)
print(f"User's path has {len(expected_path)} positions")
print(f"My path has {len(path)} positions")
print(f"\nUser says collisions at steps 6,7: (-5,2) and (-5,3)")
print(f"Let me check if those positions appear in my path...")

for i, (x, y) in enumerate(path):
    if (x, y) == (-5, 2) or (x, y) == (-5, 3):
        dx = abs(x - asteroid_x)
        dy = abs(y - asteroid_y)
        print(f"  Step {i}: ({x},{y}), dx={dx}, dy={dy} - FOUND!")
