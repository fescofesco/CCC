"""Check if positions (1,2) or (5,2) appear in our path."""
import sys
sys.path.insert(0, r'c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5')

from level5_solution import bfs_find_path

# Test case 1
xs, ys, ax, ay = 6, 0, 3, 0

print(f"Finding path from (0,0) to ({xs},{ys}), avoiding asteroid at ({ax},{ay})")
path = bfs_find_path(xs, ys, ax, ay)

print(f"\nPath ({len(path)} positions):")
for i, (x, y) in enumerate(path):
    dist = max(abs(x - ax), abs(y - ay))
    if (x, y) in [(1, 2), (5, 2)]:
        print(f"  {i}: ({x}, {y}) - distance: {dist} *** CORNER POSITION ***")
    else:
        print(f"  {i}: ({x}, {y}) - distance: {dist}")

# Check if corners are in path
corner1 = (1, 2) in path
corner2 = (5, 2) in path

print(f"\nCorner (1,2) in path: {corner1}")
print(f"Corner (5,2) in path: {corner2}")

# Verify these corners should be forbidden
dist1 = max(abs(1 - ax), abs(2 - ay))
dist2 = max(abs(5 - ax), abs(2 - ay))
print(f"\nDistance from (1,2) to asteroid: {dist1} - Forbidden? {dist1 <= 2}")
print(f"Distance from (5,2) to asteroid: {dist2} - Forbidden? {dist2 <= 2}")
