"""Debug the BFS path finding."""
import sys
sys.path.insert(0, r'c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5')

from level5_solution import bfs_find_path, is_forbidden_cell

# Test case 1
xs, ys, ax, ay = 6, 0, 3, 0

print(f"Target: ({xs}, {ys})")
print(f"Asteroid: ({ax}, {ay})")
print(f"\nChecking if cells are forbidden (distance <= 2):")

# Check some key positions
positions = [
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3)
]

print("\nForbidden cells (within distance 2 of asteroid):")
for pos in positions:
    if is_forbidden_cell(pos[0], pos[1], ax, ay):
        dist = max(abs(pos[0] - ax), abs(pos[1] - ay))
        print(f"  {pos} - distance: {dist}")

print("\nFinding path with BFS...")
try:
    path = bfs_find_path(xs, ys, ax, ay)
    print(f"Path found with {len(path)} positions:")
    for i, (x, y) in enumerate(path):
        dist = max(abs(x - ax), abs(y - ay))
        forbidden = "FORBIDDEN!" if dist <= 2 else "OK"
        print(f"  {i}: ({x}, {y}) - distance to asteroid: {dist} - {forbidden}")
except Exception as e:
    print(f"Error: {e}")
