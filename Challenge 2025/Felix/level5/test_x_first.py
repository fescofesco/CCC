import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from level5 import generate_sequence, get_path_from_sequences, check_asteroid_collision

target_x, target_y = 2, 10
asteroid_x, asteroid_y = 1, 4

x_seq = generate_sequence(target_x, 200)
y_seq = generate_sequence(target_y, 200)

print(f"X sequence: {x_seq}")
print(f"Y sequence: {y_seq}")

# Strategy: X completes first (reaches X=2), THEN Y moves
# X moves while Y waits, then Y moves while X waits

x_move_then_wait = x_seq + [0] * (len(y_seq) - 2)
y_wait_then_move = [0] * (len(x_seq) - 1) + y_seq[1:]

max_len = max(len(x_move_then_wait), len(y_wait_then_move))
x_padded = x_move_then_wait + [0] * (max_len - len(x_move_then_wait))
y_padded = y_wait_then_move + [0] * (max_len - len(y_wait_then_move))

print(f"\nX final: {x_padded}")
print(f"Y final: {y_padded}")

path = get_path_from_sequences(x_padded, y_padded)

print("\nPath:")
for i, (x, y) in enumerate(path):
    in_zone = abs(x - asteroid_x) <= 2 and abs(y - asteroid_y) <= 2
    marker = " <--- COLLISION" if in_zone else ""
    print(f"Step {i}: ({x}, {y}){marker}")

has_collision, details = check_asteroid_collision(path, asteroid_x, asteroid_y)
print(f"\nCollision: {has_collision}")
