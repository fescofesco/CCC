"""Trace step by step to find what happens at step 10."""

x_seq = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
y_seq = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

ax, ay = 3, 0

print("Step-by-step simulation:")
print("="*80)

x_pos, y_pos = 0, 0
print(f"Initial (before step 0): pos=({x_pos},{y_pos}) dist={max(abs(x_pos-ax), abs(y_pos-ay))}")

for i in range(max(len(x_seq), len(y_seq))):
    x_pace = x_seq[i] if i < len(x_seq) else 0
    y_pace = y_seq[i] if i < len(y_seq) else 0
    
    print(f"\nStep {i}:")
    print(f"  Paces: X={x_pace}, Y={y_pace}")
    print(f"  Before move: ({x_pos},{y_pos})")
    
    # Apply movement
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    dist = max(abs(x_pos - ax), abs(y_pos - ay))
    status = "OK" if dist > 2 else "*** COLLISION ***"
    
    print(f"  After move:  ({x_pos},{y_pos}) dist={dist} {status}")
    
    if i == 10:
        print(f"\n{'='*80}")
        print(f"STEP 10 DETAILS:")
        print(f"  Position: ({x_pos},{y_pos})")
        print(f"  Distance to asteroid ({ax},{ay}): {dist}")
        print(f"  Collision: {dist <= 2}")
        print(f"{'='*80}")

print("\n\nWait... maybe the validator interprets movement differently?")
print("Let me check if maybe BOTH X and Y paces are read from the SAME index...")
print("="*80)

print("\nAlternative interpretation: Both sequences at same index")
x_pos, y_pos = 0, 0

for i in range(min(len(x_seq), len(y_seq))):
    x_pace = x_seq[i]
    y_pace = y_seq[i]
    
    if i == 10:
        print(f"\nStep {i}: X_pace={x_pace}, Y_pace={y_pace}")
        print(f"  Before: ({x_pos},{y_pos})")
    
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    if i == 10:
        dist = max(abs(x_pos - ax), abs(y_pos - ay))
        print(f"  After: ({x_pos},{y_pos}) dist={dist}")
