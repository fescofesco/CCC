import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from level5.py
from level5 import generate_sequence, get_path_from_sequences, check_asteroid_collision

target_x, target_y = 2, 10
asteroid_x, asteroid_y = 1, 4

x_seq = generate_sequence(target_x, 200)
y_seq = generate_sequence(target_y, 200)

print(f"X sequence: {x_seq}")
print(f"Y sequence: {y_seq}")

# Pad to same length
max_len = max(len(x_seq), len(y_seq))
x_padded = x_seq + [0] * (max_len - len(x_seq))
y_padded = y_seq + [0] * (max_len - len(y_seq))

print(f"\nX padded: {x_padded}")
print(f"Y padded: {y_padded}")

# Get path
path = get_path_from_sequences(x_padded, y_padded)
print(f"\nPath: {path[:10]}...")  # First 10 steps

# Check collision
has_collision, details = check_asteroid_collision(path, asteroid_x, asteroid_y)
print(f"\nCollision: {has_collision}")
if has_collision:
    print(f"Details: {details[:5]}")  # First 5 collision points
