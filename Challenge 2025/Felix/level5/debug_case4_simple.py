# Read case 4 from input
with open('../../Input/level5/level5_1_small.in', 'r') as f:
    lines = f.readlines()

# Parse case 4 (lines 7-8, case index 3, but file has 2 lines per case + 1 header)
# Header line 0, case 1 lines 1-2, case 2 lines 3-4, case 3 lines 5-6, case 4 lines 7-8
target_line = lines[7].strip().split()
asteroid_line = lines[8].strip()

target_x, target_y = map(int, target_line[0].split(','))
time_limit = int(target_line[1])
asteroid_x, asteroid_y = map(int, asteroid_line.split(','))

print(f"Case 4:")
print(f"  Target: ({target_x}, {target_y})")
print(f"  Asteroid: ({asteroid_x}, {asteroid_y})")
print(f"  Time limit: {time_limit}")

# Read output (case 4 with blank lines = lines 9-10)
with open('../../Felix/Outputs/level5/level5_1_small.out', 'r') as f:
    output_lines = f.readlines()

# Parse sequences - each case uses 2 lines + 1 blank line = 3 lines per case
# Case 1: lines 0-1, Case 2: lines 3-4, Case 3: lines 6-7, Case 4: lines 9-10
x_seq = list(map(int, output_lines[9].strip().split()))
y_seq = list(map(int, output_lines[10].strip().split()))

print(f"\nX sequence length: {len(x_seq)}")
print(f"Y sequence length: {len(y_seq)}")
print(f"First 20 X: {x_seq[:20]}")
print(f"First 20 Y: {y_seq[:20]}")

# Calculate path
def get_path(x_seq, y_seq):
    x, y = 0, 0
    path = [(x, y)]
    for dx, dy in zip(x_seq, y_seq):
        if dx > 0:
            x += 1
        elif dx < 0:
            x -= 1
        if dy > 0:
            y += 1
        elif dy < 0:
            y -= 1
        path.append((x, y))
    return path

path = get_path(x_seq, y_seq)

# Find collisions
print(f"\nChecking for collisions near asteroid ({asteroid_x}, {asteroid_y}):")
collision_count = 0
for t, (x, y) in enumerate(path):
    dist = max(abs(x - asteroid_x), abs(y - asteroid_y))
    if dist <= 2:
        collision_count += 1
        if collision_count <= 10:  # Show first 10 collisions
            print(f"  Time {t}: Position ({x},{y}), Chebyshev dist = {dist} ← COLLISION!")

print(f"\nTotal collisions: {collision_count}")
print(f"Final position: {path[-1]}")
print(f"Time used: {len(x_seq)}")
