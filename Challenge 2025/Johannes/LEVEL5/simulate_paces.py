"""Carefully simulate the pace sequences to find the issue."""

# Our generated output for test case 1
x_seq = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
y_seq = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

ax, ay = 3, 0  # Asteroid position

print("Simulating movement step by step:")
print("="*80)

x_pos, y_pos = 0, 0
print(f"Start: ({x_pos}, {y_pos})")

max_steps = max(len(x_seq), len(y_seq))

for i in range(max_steps):
    x_pace = x_seq[i] if i < len(x_seq) else 0
    y_pace = y_seq[i] if i < len(y_seq) else 0
    
    print(f"\nStep {i}: Paces X={x_pace:2d}, Y={y_pace:2d}")
    
    # IMPORTANT: Check position BEFORE applying movement
    dist_before = max(abs(x_pos - ax), abs(y_pos - ay))
    print(f"  Before move: ({x_pos}, {y_pos}) - distance: {dist_before}")
    
    # Apply movement
    if x_pace > 0:
        x_pos += 1
    elif x_pace < 0:
        x_pos -= 1
        
    if y_pace > 0:
        y_pos += 1
    elif y_pace < 0:
        y_pos -= 1
    
    # Check position AFTER applying movement
    dist_after = max(abs(x_pos - ax), abs(y_pos - ay))
    status = "✅ OK" if dist_after > 2 else "❌ COLLISION!"
    
    print(f"  After move:  ({x_pos}, {y_pos}) - distance: {dist_after} {status}")

print(f"\n{'='*80}")
print(f"Final position: ({x_pos}, {y_pos})")
print(f"Target: (6, 0)")
print(f"Match: {(x_pos, y_pos) == (6, 0)}")
