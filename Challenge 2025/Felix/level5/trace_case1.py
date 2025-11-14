def trace_path():
    x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
    y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]
    
    x, y = 0, 0
    asteroid_x, asteroid_y = -3, 4
    
    print(f"Asteroid at: ({asteroid_x}, {asteroid_y})")
    print(f"Forbidden zone (radius 2): all positions where max(|x-({asteroid_x})|, |y-({asteroid_y})|) <= 2")
    print(f"Starting position: ({x}, {y})")
    print()
    
    # Starting position check
    dist = max(abs(x - asteroid_x), abs(y - asteroid_y))
    collision = dist <= 2
    print(f"Start   : Position ({x:3d}, {y:3d}), Distance={dist}, {'COLLISION!' if collision else 'OK'}")
    
    for step, (x_pace, y_pace) in enumerate(zip(x_seq, y_seq), 1):
        # Pace determines direction: move 1 square per step
        if x_pace > 0:
            x += 1
        elif x_pace < 0:
            x -= 1
        
        if y_pace > 0:
            y += 1
        elif y_pace < 0:
            y -= 1
        
        # Check collision
        dist = max(abs(x - asteroid_x), abs(y - asteroid_y))
        collision = dist <= 2
        
        dx = abs(x - asteroid_x)
        dy = abs(y - asteroid_y)
        
        # Check if this is the problematic diagonal case
        is_diagonal_2 = (dx == 2 and dy == 2)
        
        print(f"Step {step:2d}: X_pace={x_pace:2d}, Y_pace={y_pace:2d} -> Position ({x:3d}, {y:3d}), dx={dx}, dy={dy}, Chebyshev={dist}, {'DIAGONAL-2!' if is_diagonal_2 else 'COLLISION!' if collision else 'OK'}")
        
        if collision or is_diagonal_2:
            print(f"  *** FORBIDDEN! Spaceship at ({x}, {y}) is within radius 2 of asteroid at ({asteroid_x}, {asteroid_y})")

trace_path()
