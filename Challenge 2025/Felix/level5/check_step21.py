"""Check collision at step 21 for case 15"""

# Step 21: ship at (4, 5)
# Asteroid at (6, 2)

ship_pos = (4, 5)
asteroid_pos = (6, 2)

dx = abs(ship_pos[0] - asteroid_pos[0])
dy = abs(ship_pos[1] - asteroid_pos[1])

print(f"Step 21: Ship at {ship_pos}, Asteroid at {asteroid_pos}")
print(f"dx = |4 - 6| = {dx}")
print(f"dy = |5 - 2| = {dy}")
print(f"Chebyshev distance = max({dx}, {dy}) = {max(dx, dy)}")
print()

if dx <= 2 and dy <= 2:
    print("❌ COLLISION! Both dx ≤ 2 AND dy ≤ 2")
    print(f"   Forbidden zone: asteroid at (6,2) blocks all positions where |x-6|≤2 AND |y-2|≤2")
    print(f"   Position (4,5): dx=2 ✓, dy=3 ✓ -> dy > 2, so NO collision actually!")
else:
    print("✅ NO COLLISION")
    if dx > 2:
        print(f"   dx = {dx} > 2")
    if dy > 2:
        print(f"   dy = {dy} > 2")
