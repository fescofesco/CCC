"""
Maybe each pace causes MULTIPLE position checks during movement?

For example, if pace=5 means "move +1 over 5 time units", maybe
we need to check collision at EVERY time step, not just when
the position changes?

Let me check the Level 3 logic to understand movement better.
"""

print("Question: Does a single pace value cause ONE position change,")
print("or does it cause position checks at every time unit?")
print()
print("From Level 3 understanding:")
print("- Pace 5: Move +1 position, costs 5 time units")
print("- The movement happens in ONE step, not gradually")
print()
print("So for pace sequence [0, 5, 4, 5]:")
print("  Step 0: pace=0, stay at current position, time += 1")
print("  Step 1: pace=5, move +1 position, time += 5")
print("  Step 2: pace=4, move +1 position, time += 4")
print("  Step 3: pace=5, move +1 position, time += 5")
print()
print("The position changes happen DISCRETELY at each step,")
print("not continuously over time.")
print()
print("Therefore, we should check collision at each POSITION,")
print("which is what we're already doing!")
print()
print("="*60)
print("Unless... wait, let me check if the STARTING position")
print("(before any pace is applied) also needs to avoid collision")
print("="*60)

# Check starting position
ax, ay = 3, 0
start_x, start_y = 0, 0
dist_start = max(abs(start_x - ax), abs(start_y - ay))

print(f"\nStarting position: ({start_x}, {start_y})")
print(f"Asteroid at: ({ax}, {ay})")
print(f"Distance: {dist_start}")
print(f"Safe? {dist_start > 2}")

if dist_start > 2:
    print("\n✅ Starting position is safe!")
else:
    print("\n❌ Starting position is in collision zone!")
