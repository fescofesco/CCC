from dataclasses import dataclass
from typing import List


@dataclass
class RoomDeskInfo:
    x: int  # Room length (x-axis)
    y: int  # Room height (y-axis)
    desk_count: int  # Total number of desks that can fit
    id: int  # Room ID


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
        room_infos.append(RoomDeskInfo(x, y, desk_count, i))
    return room_infos

def provide_room_id_matrix(room_infos: List[RoomDeskInfo]) -> List[str]:
    """Generate the room matrix filling desk IDs and empty spaces."""
    results = []

    for room_info in room_infos:
        x, y, desk_count = room_info.x, room_info.y, room_info.desk_count
        matrix = [[0] * x for _ in range(y)]  # Create a grid initialized with 0 (empty cells)

        desk_id = 1
        desks_placed = 0  # To track the number of desks placed (each desk = 3 units)

        # Place desks in full rows (groups of 3 in x)
        for row in range(y):
            for i in range(0, x - x % 3, 3):  # Iterate over columns in steps of 3
                if desks_placed < desk_count:
                    matrix[row][i] = desk_id
                    matrix[row][i + 1] = desk_id
                    matrix[row][i + 2] = desk_id
                    desk_id += 1
                    desks_placed += 1

        remainder_cols = x % 3
        if remainder_cols > 0:
            for col in range(x - remainder_cols, x):  # For the remaining 1 or 2 columns
                for row in range(y):
                    if desks_placed < desk_count:
                        matrix[row][col] = desk_id
                        if (row + 1) % 3 == 0:  # Move to a new desk ID after filling 3 cells vertically
                            desk_id += 1
                            desks_placed += 1

        # Formatting the matrix output to match the required format
        matrix_output = '\n'.join(' '.join(map(str, row)) for row in matrix)
        results.append(matrix_output)

    return results


def format_output(room_results: List[str]) -> str:
    """Format the results by joining the room matrices."""
    return '\n\n'.join(room_results)


if __name__ == '__main__':
    import os
    from pathlib import Path

    input_location = Path("../Inputs/level3")
    output_location = Path("../Outputs/level3")

    # Load input files
    input_files = load_inputs(input_location)

    for f_p in input_files:
        with open(f_p, "r") as file:
            input_string = file.read()

        # Parse input
        rooms = parse_input(input_string)

        # Generate the room matrices with desk IDs and empty spaces
        room_results = provide_room_id_matrix(rooms)

        # Format the output
        formatted_output = format_output(room_results)

        # Write the output to the corresponding file
        out_fp = output_location / (Path(f_p).stem + ".out")
        with open(out_fp, "w") as file:
            file.write(formatted_output)
