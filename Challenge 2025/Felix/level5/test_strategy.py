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

# Move X only after Y reaches Y > 6 (past asteroid safety zone)
# Y reaches position 5 at step 6 (0-indexed)
# Y reaches position 6 at step 7
# Y reaches position 7 at step 8 - This is past the asteroid zone (4±2)

# So we need to delay X until step 8 or later
# That means insert X sequence after 8 steps of Y

y_wait_then_x = y_seq[:8] + [0] * (len(x_seq) - 1)  # Y moves for 8 steps, then waits while X moves
x_wait_then_move = [0] * 8 + x_seq[1:]  # X waits for 8 steps, then moves

# Combine
max_len = max(len(x_wait_then_move), len(y_wait_then_x))
x_padded = x_wait_then_move + [0] * (max_len - len(x_wait_then_move))
y_padded = y_wait_then_x + [0] * (max_len - len(y_wait_then_x))

print(f"\nX final: {x_padded}")
print(f"Y final: {y_padded}")

path = get_path_from_sequences(x_padded, y_padded)
has_collision, details = check_asteroid_collision(path, asteroid_x, asteroid_y)

print(f"\nCollision: {has_collision}")
if has_collision:
    print(f"Details: {details[:5]}")
else:
    print(f"Success! Path: {path}")
