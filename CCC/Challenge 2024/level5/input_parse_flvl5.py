from dataclasses import dataclass
from typing import List
import math


@dataclass
class RoomDeskInfo:
    x: int  # Room length (x-axis)
    y: int  # Room height (y-axis)
    desks_to_place: int  # Fixed number of desks to place


def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory."""
    input_files = []
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files


def parse_input(input_string):
    """Parse the input format where each line gives room dimensions and number of desks."""
    lines = input_string.strip().split('\n')
    N = int(lines[0])  # Number of rooms

    room_infos = []
    for i in range(1, N + 1):
        x, y, desk_count = map(int, lines[i].split())
        room_infos.append(RoomDeskInfo(x, y, desk_count))
    return room_infos


def provide_room_matrix(room_infos: List[RoomDeskInfo]) -> List[str]:
    """Generate the room matrix with the specified number of desks without touching each other."""
    results = []

    for room_info in room_infos:
        x, y, desk_count = room_info.x, room_info.y, room_info.desks_to_place
        matrix = [['.'] * x for _ in range(y)]
        desks_placed = 0

        # Calculate potential desk placements for both orientations
        horizontal_capacity = (y + 1) // 2 * (x // 3)
        vertical_capacity = (x + 1) // 2 * (y // 3)

        # Decide whether to place desks horizontally or vertically
        start_horizontally = horizontal_capacity >= vertical_capacity

        if start_horizontally:
            # Place desks horizontally
            for row in range(0, y, 2):  # Every other row to prevent adjacency
                for col in range(0, x - 1, 3):  # Place desks with spacing
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                    if col + 1 < x:
                        matrix[row][col] = 'X'
                        matrix[row][col + 1] = 'X'
                        desks_placed += 1
                if desks_placed >= desk_count:
                    break
        else:
            # Place desks vertically
            for col in range(0, x, 2):  # Every other column to prevent adjacency
                for row in range(0, y - 1, 3):  # Place desks with spacing
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                    if row + 1 < y:
                        matrix[row][col] = 'X'
                        matrix[row + 1][col] = 'X'
                        desks_placed += 1
                if desks_placed >= desk_count:
                    break

        # Convert the matrix to the required output format
        matrix_output = '\n'.join(''.join(row) for row in matrix)
        results.append(matrix_output)
        if desks_placed < room_info.desks_to_place:
            print("Not all desks could be placed.")

    return results


def format_output(room_results: List[str]) -> str:
    """Format the results by joining the room matrices."""
    return '\n\n'.join(room_results)


if __name__ == '__main__':
    import os
    from pathlib import Path

    input_location = Path("../Inputs/level5")
    output_location = Path("../Outputs/level5")

    # Load input files
    input_files = load_inputs(input_location)

    for f_p in input_files:
        with open(f_p, "r") as file:
            input_string = file.read()

        # Parse input
        rooms = parse_input(input_string)

        # Generate the room matrices with desks and empty spaces
        room_results = provide_room_matrix(rooms)

        # Format the output
        formatted_output = format_output(room_results)

        # Write the output to the corresponding file
        out_fp = output_location / (Path(f_p).stem + ".out")
        with open(out_fp, "w") as file:
            file.write(formatted_output)