import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from level5 import generate_sequence, get_path_from_sequences, check_asteroid_collision

target_x, target_y = 2, 10
asteroid_x, asteroid_y = 1, 4

x_seq = generate_sequence(target_x, 200)
y_seq = generate_sequence(target_y, 200)

print(f"X sequence: {x_seq} (len={len(x_seq)})")
print(f"Y sequence: {y_seq} (len={len(y_seq)})")

# Strategy: Y completes first, THEN X moves
# X waits while Y completes, then X moves while Y waits at target

x_wait_then_move = [0] * (len(y_seq) - 1) + x_seq[1:]
y_move_then_wait = y_seq + [0] * (len(x_seq) - 2)

# Make same length
max_len = max(len(x_wait_then_move), len(y_move_then_wait))
x_padded = x_wait_then_move + [0] * (max_len - len(x_wait_then_move))
y_padded = y_move_then_wait + [0] * (max_len - len(y_move_then_wait))

print(f"\nX final: {x_padded}")
print(f"Y final: {y_padded}")
print(f"Lengths: X={len(x_padded)}, Y={len(y_padded)}")

path = get_path_from_sequences(x_padded, y_padded)
has_collision, details = check_asteroid_collision(path, asteroid_x, asteroid_y)

print(f"\nCollision: {has_collision}")
if has_collision:
    print(f"Details: {details[:5]}")
else:
    print(f"Success!")
    print(f"Final position: {path[-1]}")
