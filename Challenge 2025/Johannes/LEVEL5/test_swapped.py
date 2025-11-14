"""
Maybe the validator is interpreting the sequences in reverse order?
Or maybe it's reading Y first, then X?
"""

# Our output
x_seq = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
y_seq = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

ax, ay = 3, 0

print("HYPOTHESIS: Maybe Y sequence is first in the file, not X?")
print("="*80)

# Swap them
y_pos, x_pos = 0, 0  # Start at (0,0) but with Y,X swapped

print(f"Initial: pos=({x_pos},{y_pos})")

for i in range(max(len(x_seq), len(y_seq))):
    # If Y is first line, X is second line
    y_pace = x_seq[i] if i < len(x_seq) else 0  # First line
    x_pace = y_seq[i] if i < len(y_seq) else 0  # Second line
    
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
    
    if i <= 12 or dist <= 2:
        print(f"Step {i:2d}: paces(Y={y_pace:2d},X={x_pace:2d}) -> pos({x_pos:2d},{y_pos:2d}) dist={dist} {status}")
    
    if i == 10:
        print(f"\n{'='*60}")
        print(f"At step 10: Position ({x_pos},{y_pos})")
        print(f"Expected collision position: (1,2)")
        print(f"Match? {(x_pos, y_pos) == (1, 2)}")
        print(f"{'='*60}\n")

print("\n" + "="*80)
print("Checking if we ever reach (1,2)...")
print("="*80)

# Reset and check all positions with swapped interpretation
y_pos, x_pos = 0, 0
all_positions = [(x_pos, y_pos)]

for i in range(max(len(x_seq), len(y_seq))):
    y_pace = x_seq[i] if i < len(x_seq) else 0
    x_pace = y_seq[i] if i < len(y_seq) else 0
    
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    all_positions.append((x_pos, y_pos))
    
    if (x_pos, y_pos) == (1, 2):
        print(f"Position (1,2) reached at step {i}!")
        dist = max(abs(x_pos - ax), abs(y_pos - ay))
        print(f"Distance to asteroid: {dist}")

print(f"\nAll positions with swapped interpretation: {set(all_positions)}")
