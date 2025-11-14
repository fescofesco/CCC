"""Test: Pace = time spent traveling, position changes by ±1 when pace≠0."""

x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

asteroid_x, asteroid_y = -3, 4

print("CORRECT INTERPRETATION: Pace = time cost")
print(f"Asteroid at ({asteroid_x}, {asteroid_y})\n")
print("When pace ≠ 0: move ±1 in that dimension")
print("Time cost = |pace| if pace≠0, or 1 if pace=0")
print("="*70)

x, y = 0, 0
time = 0

path_with_time = []

for i in range(len(x_seq)):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    # Calculate time cost for this pace
    if x_pace == 0:
        x_time = 1
    else:
        x_time = abs(x_pace)
    
    if y_pace == 0:
        y_time = 1
    else:
        y_time = abs(y_pace)
    
    # Time cost is the MAX of the two (they happen simultaneously)
    time_cost = max(x_time, y_time)
    
    # Move once if pace is non-zero
    if x_pace > 0:
        x += 1
    elif x_pace < 0:
        x -= 1
    
    if y_pace > 0:
        y += 1
    elif y_pace < 0:
        y -= 1
    
    # We spend time_cost time units at this position
    for t in range(time_cost):
        time += 1
        path_with_time.append((time, x, y))
        
        dx = abs(x - asteroid_x)
        dy = abs(y - asteroid_y)
        collision = (dx <= 2 and dy <= 2)
        
        if time <= 45:  # Show first 45 steps
            print(f"Step {time:2d}: pos=({x:3d},{y:3d}), dx={dx}, dy={dy}, {'COLLISION!' if collision else 'OK'}")

print(f"\nTotal time: {time}")
print(f"Final position: ({x}, {y})")
print(f"Target: (-6, 9)")
