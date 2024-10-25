from dataclasses import dataclass
from typing import List
import os


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
    """Generate the room matrix with the specified number of desks in 1x3 blocks without touching each other."""
    results = []

    for room_info in room_infos:
        x, y, desk_count = room_info.x, room_info.y, room_info.desks_to_place
        matrix = [['.'] * x for _ in range(y)]
        desks_placed = 0

        place_horizontally = x >= y  # Place 1x3 blocks along the larger dimension
        max_primary_dim = x if place_horizontally else y
        max_secondary_dim = y if place_horizontally else x

        # Place desks in 1x3 blocks in every second row or column
        for primary in range(0, max_secondary_dim, 2):
            for secondary in range(0, max_primary_dim - 2, 4):  # Step by 4 to leave space
                if desks_placed >= desk_count:
                    break
                if place_horizontally:
                    # Horizontal placement of 1x3 blocks in every second row
                    matrix[primary][secondary] = 'X'
                    matrix[primary][secondary + 1] = 'X'
                    matrix[primary][secondary + 2] = 'X'
                else:
                    # Vertical placement of 1x3 blocks in every second column
                    matrix[secondary][primary] = 'X'
                    matrix[secondary + 1][primary] = 'X'
                    matrix[secondary + 2][primary] = 'X'
                desks_placed += 1

        # Formatting the matrix output
        matrix_output = '\n'.join(''.join(row) for row in matrix)
        results.append(matrix_output)

    return results


def format_output(room_results: List[str]) -> str:
    """Format the results by joining the room matrices."""
    return '\n\n'.join(room_results)


if __name__ == '__main__':
    from pathlib import Path

    input_location = Path("../Inputs/level4")
    output_location = Path("../Outputs/level4")

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
