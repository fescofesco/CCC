import sys
sys.path.append('../level3')
from class_Data_Level_loader import DataLevelLoader

# Load the small input file  
loader = DataLevelLoader(level=5)
data = loader.load_input('../../Input/level5/level5_1_small.in')

# Get case 4 (index 3)
case = data[3]
print(f"Case 4:")
print(f"  Target: ({case['target_x']}, {case['target_y']})")
print(f"  Asteroid: ({case['asteroid_x']}, {case['asteroid_y']})")
print(f"  Time limit: {case['time_limit']}")

# Read the output
with open('../../Felix/Outputs/level1/level5_1_small.out', 'r') as f:
    lines = f.readlines()
    
# Line 4 (index 3) contains case 4 output
x_seq = list(map(int, lines[3].split()[0].split(',')))
y_seq = list(map(int, lines[3].split()[1].split(',')))

print(f"\nX sequence: {x_seq[:20]}... (len={len(x_seq)})")
print(f"Y sequence: {y_seq[:20]}... (len={len(y_seq)})")

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
ax, ay = case['asteroid_x'], case['asteroid_y']

# Find collision
print(f"\nChecking for collisions near asteroid ({ax}, {ay}):")
for t, (x, y) in enumerate(path):
    dist = max(abs(x - ax), abs(y - ay))
    if dist <= 2:
        print(f"  Time {t}: Position ({x},{y}), Chebyshev dist = {dist} {'← COLLISION!' if dist <= 2 else ''}")
