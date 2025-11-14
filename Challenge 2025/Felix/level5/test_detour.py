import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def calculate_position_and_time(sequence):
    """Calculate position and time using level2 logic."""
    position = 0
    total_time = 0
    
    for pace in sequence:
        if pace > 0:
            position += 1
            total_time += pace
        elif pace < 0:
            position -= 1
            total_time += abs(pace)
        else:
            total_time += 1
    
    return position, total_time


# Test detour creation
detour_distance = 3
direction = 1

# Detour sequence: go up/down then come back
detour_seq = [0, 5 * direction, 4 * direction, 5 * direction, 0]  # Should move 3 units
print("Initial detour:", detour_seq)
print("Position:", calculate_position_and_time(detour_seq)[0])

# Create return journey
return_seq = [0]
return_distance = abs(calculate_position_and_time(detour_seq)[0])
for _ in range(return_distance):
    return_seq.append(-5 * direction)
return_seq.append(0)

print("Return seq:", return_seq)
print("Return position:", calculate_position_and_time(return_seq)[0])

# Full detour
full_detour = detour_seq[:-1] + return_seq
print("Full detour:", full_detour)
print("Final position:", calculate_position_and_time(full_detour)[0])
