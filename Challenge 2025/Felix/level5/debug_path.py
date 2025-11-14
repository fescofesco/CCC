import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from level5 import generate_sequence, get_path_from_sequences, check_asteroid_collision

target_x, target_y = 2, 10
asteroid_x, asteroid_y = 1, 4

x_seq = generate_sequence(target_x, 200)
y_seq = generate_sequence(target_y, 200)

x_wait_then_move = [0] * (len(y_seq) - 1) + x_seq[1:]
y_move_then_wait = y_seq + [0] * (len(x_seq) - 2)

max_len = max(len(x_wait_then_move), len(y_move_then_wait))
x_padded = x_wait_then_move + [0] * (max_len - len(x_wait_then_move))
y_padded = y_move_then_wait + [0] * (max_len - len(y_move_then_wait))

path = get_path_from_sequences(x_padded, y_padded)

print("Path:")
for i, (x, y) in enumerate(path):
    # Check if within asteroid zone
    in_zone = abs(x - asteroid_x) <= 2 and abs(y - asteroid_y) <= 2
    marker = " <--- COLLISION" if in_zone else ""
    print(f"Step {i}: ({x}, {y}){marker}")
