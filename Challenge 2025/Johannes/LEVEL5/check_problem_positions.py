"""Check if these specific positions are in our path."""

# Our generated sequences
x_seq = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
y_seq = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

ax, ay = 3, 0

# Check distances for the problem positions
problem_positions = [(1, 2), (2, 2), (5, 2)]

print("Checking problem positions:")
for px, py in problem_positions:
    dist = max(abs(px - ax), abs(py - ay))
    print(f"  ({px}, {py}): distance = max(|{px}-3|, |{py}-0|) = max({abs(px-3)}, {abs(py-0)}) = {dist}")
    print(f"           {'FORBIDDEN (collision)' if dist <= 2 else 'Safe'}")

print("\n" + "="*80)
print("Simulating our generated sequences:")
print("="*80)

x_pos, y_pos = 0, 0
all_positions = [(x_pos, y_pos)]

for i in range(max(len(x_seq), len(y_seq))):
    x_pace = x_seq[i] if i < len(x_seq) else 0
    y_pace = y_seq[i] if i < len(y_seq) else 0
    
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    all_positions.append((x_pos, y_pos))
    dist = max(abs(x_pos - ax), abs(y_pos - ay))
    
    if (x_pos, y_pos) in problem_positions:
        print(f"Step {i}: ({x_pos},{y_pos}) dist={dist} *** PROBLEM POSITION ***")

print("\n" + "="*80)
print("Summary:")
print("="*80)
print(f"All unique positions visited: {set(all_positions)}")
print()
for pos in problem_positions:
    if pos in all_positions:
        print(f"ERROR: Position {pos} WAS visited!")
    else:
        print(f"OK: Position {pos} was NOT visited")

print("\n" + "="*80)
print("Wait - did you mean (5,5) or (5,2)?")
print("="*80)
if (5, 5) in all_positions:
    print("(5,5) was visited")
else:
    print("(5,5) was NOT visited")
