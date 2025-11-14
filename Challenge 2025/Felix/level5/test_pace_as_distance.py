"""Test: Both dimensions move simultaneously when both paces are non-zero."""

x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

asteroid_x, asteroid_y = -3, 4

print("NEW INTERPRETATION: Move in BOTH dimensions when BOTH paces are non-zero")
print(f"Asteroid at ({asteroid_x}, {asteroid_y})\n")

x, y = 0, 0

for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    # Move in BOTH dimensions if BOTH have pace
    # Actually wait - looking at the sequences:
    # X: 0 -5 -4 -3 -2 -3 -4 -5 0 0 0 0 0 0 0 0 0 5 0 0
    # Y: 0  0  0  0  0  0  0  0 0 5 4 3 2 1 2 3 4 5 0 0
    
    # At step 4: X=-2, Y=0 - only X moves
    # But user shows step 4 as (-3, 1), meaning Y moved too!
    
    # Wait, maybe the pace affects the ACCELERATION or velocity change?
    # Let me think... if pace represents velocity, then position += velocity * time
    # But time is always 1 per step...
    
    # OR - maybe we move at the pace VALUE, not just +/-1?
    
    print(f"Step {i}: pace=({x_pace:2d},{y_pace:2d})")

print("\nLet me try: position changes by the PACE value itself")
print("="*70)

x, y = 0, 0
for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    # Move by the pace value
    x += x_pace
    y += y_pace
    
    dx = abs(x - asteroid_x)
    dy = abs(y - asteroid_y)
    collision = (dx <= 2 and dy <= 2)
    
    print(f"Step {i:2d}: pace=({x_pace:2d},{y_pace:2d}) → ({x:3d},{y:3d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")
