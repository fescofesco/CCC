import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from level5 import generate_sequence, get_path_from_sequences, check_asteroid_collision, calculate_position_and_time

target_x, target_y = 2, 10
asteroid_x, asteroid_y = 1, 4

# X strategy: Go to X=4 (past asteroid), stay there while Y moves, then come back to X=2
# To reach X=4: 0 -> 5,4,5,5 -> 0 (moves to position 4)
x_detour_right = [0, 5, 4, 5, 5, 0]
pos_x, _ = calculate_position_and_time(x_detour_right)
print(f"X detour right to {pos_x}: {x_detour_right}")

# Return from X=4 to X=2: 0 -> -5,-5 -> 0 (moves -2)
x_return_left = [0, -5, -5, 0]
pos_return, _ = calculate_position_and_time(x_return_left)
print(f"X return {pos_return}: {x_return_left}")

# Y strategy: normal movement to Y=10
y_seq = generate_sequence(target_y, 200)
print(f"Y sequence: {y_seq}")

# Combine: X goes right, Y waits. Then Y moves, X waits. Then X comes back, Y waits.
x_combined = x_detour_right[:-1] + [0] * (len(y_seq) - 2) + x_return_left[1:]
y_combined = [0] * (len(x_detour_right) - 1) + y_seq + [0] * (len(x_return_left) - 2)

# Pad to same length
max_len = max(len(x_combined), len(y_combined))
x_padded = x_combined + [0] * (max_len - len(x_combined))
y_padded = y_combined + [0] * (max_len - len(y_combined))

print(f"\nX final: {x_padded}")
print(f"Y final: {y_padded}")
print(f"Lengths: {len(x_padded)}, {len(y_padded)}")

path = get_path_from_sequences(x_padded, y_padded)

print("\nPath:")
for i, (x, y) in enumerate(path):
    in_zone = abs(x - asteroid_x) <= 2 and abs(y - asteroid_y) <= 2
    marker = " <--- COLLISION" if in_zone else ""
    print(f"Step {i}: ({x}, {y}){marker}")

has_collision, details = check_asteroid_collision(path, asteroid_x, asteroid_y)
print(f"\nCollision: {has_collision}")
print(f"Final position: {path[-1]}")
