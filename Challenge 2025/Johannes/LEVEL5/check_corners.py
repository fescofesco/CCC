"""Check if we're hitting the corner cells at distance exactly 2."""

# Test case 1 output
x_seq = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
y_seq = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

ax, ay = 3, 0  # Asteroid position

print("Checking EVERY position along the path:")
print("="*80)

x_pos, y_pos = 0, 0
print(f"Step -1 (initial): pos=({x_pos},{y_pos}) dist={max(abs(x_pos-ax), abs(y_pos-ay))}")

max_steps = max(len(x_seq), len(y_seq))

for i in range(max_steps):
    x_pace = x_seq[i] if i < len(x_seq) else 0
    y_pace = y_seq[i] if i < len(y_seq) else 0
    
    # Apply movement
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    # Check distance
    dist = max(abs(x_pos - ax), abs(y_pos - ay))
    
    status = "✅" if dist > 2 else "❌ COLLISION!"
    print(f"Step {i:2d}: pace=({x_pace:2d},{y_pace:2d}) -> pos=({x_pos:2d},{y_pos:2d}) dist={dist} {status}")

print("="*80)

# Now check what forbidden cells exist
print("\nAll forbidden cells (distance <= 2):")
for y in range(-2, 3):
    for x in range(1, 6):
        dist = max(abs(x - ax), abs(y - ay))
        if dist <= 2:
            print(f"  ({x}, {y}) - distance {dist}")
