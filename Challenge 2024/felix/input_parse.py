def parse_input(input_string):
    lines = input_string.strip().split('\n')
    N = int(lines[0])  # Number of rooms
    rooms = []

    # Parse each room dimension
    for i in range(1, N + 1):
        x, y = map(int, lines[i].split())
        rooms.append((x, y))

import os
from pathlib import Path
    return rooms

location = Path("../Inputs/level1")
def max_desks_in_room(x, y):
    # Desk dimensions
    desk_width = 3
    desk_height = 1

def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory."""
    input_files = []
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files
    # Maximum desks that can fit along the width and height of the room
    desks_in_width = x // desk_width
    desks_in_height = y // desk_height

    # Total desks that can fit in the room
    total_desks = desks_in_width * desks_in_height

    return total_desks

def calculate_desks(rooms):
    desk_counts = [max_desks_in_room(x, y) for x, y in rooms]
    return desk_counts

def format_output(desk_counts):
    return '\n'.join(map(str, desk_counts))

if __name__ == '__main__':
    input_string = """3
    6 5
    9 8
    6 7"""

    # Parse the input
    rooms = parse_input(input_string)

    # Calculate the number of desks for each room
    desk_counts = calculate_desks(rooms)

    # Format the output
    output_string = format_output(desk_counts)
    print(output_string)
