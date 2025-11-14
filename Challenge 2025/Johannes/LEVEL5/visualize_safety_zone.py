"""Visualize the safety zone - it's a SQUARE with radius 2."""

# For asteroid at (3, 0), show which cells are forbidden
ax, ay = 3, 0

print("Safety zone around asteroid at (3, 0):")
print("Chebyshev distance <= 2 creates a SQUARE, not a circle!")
print()

# Show a grid
for y in range(5, -3, -1):
    row = f"y={y:2d} | "
    for x in range(-1, 8):
        dist = max(abs(x - ax), abs(y - ay))
        
        if (x, y) == (ax, ay):
            row += " A "  # Asteroid
        elif dist <= 2:
            row += " X "  # Forbidden (collision zone)
        else:
            row += " . "  # Safe
    print(row)

print("       " + "---" * 9)
print("       " + "".join(f"{x:3d}" for x in range(-1, 8)))

print("\nLegend:")
print("  A = Asteroid at (3, 0)")
print("  X = Forbidden zone (Chebyshev distance <= 2)")
print("  . = Safe zone (Chebyshev distance > 2)")

print("\n" + "="*60)
print("Key insight: The diagonal cells ARE included!")
print("="*60)

# Show diagonal distances
print("\nDiagonal cells around asteroid:")
diagonals = [
    (ax - 2, ay - 2), (ax - 2, ay + 2),
    (ax + 2, ay - 2), (ax + 2, ay + 2)
]

for x, y in diagonals:
    dist = max(abs(x - ax), abs(y - ay))
    print(f"  ({x}, {y}): Chebyshev distance = max(|{x}-{ax}|, |{y}-{ay}|) = max({abs(x-ax)}, {abs(y-ay)}) = {dist}")
    print(f"           {'FORBIDDEN' if dist <= 2 else 'SAFE'}")

print("\nSo yes, diagonal cells at distance 2 ARE part of the forbidden zone!")
print("It's a 5x5 square centered on the asteroid.")
