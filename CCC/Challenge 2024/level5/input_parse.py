from dataclasses import dataclass
from typing import List


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
        x, y, desks_to_place = room_info.x, room_info.y, room_info.desks_to_place
        matrix = [['.'] * x for _ in range(y)]
        desks_placed = 0

        for i in range(y):
            for j in range(x):
                if matrix[i][j] == '.':
                    placed = False
                    # Try horizontal orientation
                    if j + 2 < x and all(matrix[i][j + k] == '.' for k in range(3)):
                        # Check adjacent cells
                        adjacent_cells = set()
                        for k in range(3):
                            ni, nj = i, j + k
                            for ai in range(ni - 1, ni + 2):
                                for aj in range(nj - 1, nj + 2):
                                    if (ai, aj) != (ni, nj) and 0 <= ai < y and 0 <= aj < x:
                                        adjacent_cells.add((ai, aj))
                        # Remove the positions of the desk itself
                        adjacent_cells -= {(i, j + k) for k in range(3)}
                        if not any(matrix[ai][aj] == 'X' for ai, aj in adjacent_cells):
                            # Place the desk
                            for k in range(3):
                                matrix[i][j + k] = 'X'
                            desks_placed += 1
                            placed = True
                    # Try vertical orientation if horizontal placement wasn't possible
                    if not placed and i + 2 < y and all(matrix[i + k][j] == '.' for k in range(3)):
                        # Check adjacent cells
                        adjacent_cells = set()
                        for k in range(3):
                            ni, nj = i + k, j
                            for ai in range(ni - 1, ni + 2):
                                for aj in range(nj - 1, nj + 2):
                                    if (ai, aj) != (ni, nj) and 0 <= ai < y and 0 <= aj < x:
                                        adjacent_cells.add((ai, aj))
                        # Remove the positions of the desk itself
                        adjacent_cells -= {(i + k, j) for k in range(3)}
                        if not any(matrix[ai][aj] == 'X' for ai, aj in adjacent_cells):
                            # Place the desk
                            for k in range(3):
                                matrix[i + k][j] = 'X'
                            desks_placed += 1
                            placed = True
                    if desks_placed >= desks_to_place:
                        break
                if desks_placed >= desks_to_place:
                    break
            if desks_placed >= desks_to_place:
                break

        # Convert the matrix to the required output format
        matrix_output = '\n'.join(''.join(row) for row in matrix)
        results.append(matrix_output)

    return results


def format_output(room_results: List[str]) -> str:
    """Format the results by joining the room matrices."""
    return '\n\n'.join(room_results)


if __name__ == '__main__':
    import os
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
