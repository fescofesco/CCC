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

# Try delaying X
for delay in range(1, 20):
    x_test = [0] * delay + x_seq
    max_len = max(len(x_test), len(y_seq))
    x_padded = x_test + [0] * (max_len - len(x_test))
    y_padded = y_seq + [0] * (max_len - len(y_seq))
    
    path = get_path_from_sequences(x_padded, y_padded)
    has_collision, details = check_asteroid_collision(path, asteroid_x, asteroid_y)
    
    if not has_collision:
        print(f"\nDelay {delay} in X works!")
        print(f"Path: {path}")
        break
    else:
        print(f"Delay {delay}: collision at {details[0]}")
