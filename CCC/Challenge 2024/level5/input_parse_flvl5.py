import copy
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

        start_horizontally = True

        desks_placed, result_mat = try_table_placement(desk_count, desks_placed, copy.deepcopy(matrix), start_horizontally, x, y)

        if room_info.desks_to_place != desks_placed:
            desks_placed, result_mat = try_table_placement(desk_count, desks_placed, matrix, not start_horizontally, x, y)
            print(f"Warning: Could not place all desks in room {x}x{y}. Placed {desks_placed} desks out of {desk_count}.")

        matrix_output = '\n'.join(''.join(row) for row in result_mat)
        results.append(matrix_output)

    return results


def try_table_placement(desk_count, desks_placed, matrix, start_horizontally, x, y):
    # Step 1: Initial Placement in Preferred Orientation
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
    # Step 2: Additional Placement in Alternative Orientation
    if desks_placed < desk_count:
        # Attempt to place additional desks in the alternative orientation
        if start_horizontally:
            # Try placing vertical desks in remaining spaces
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a vertical desk
                        if row + 1 < y and matrix[row + 1][col] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row + 1, col)]):
                                matrix[row][col] = 'X'
                                matrix[row + 1][col] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
        else:
            # Try placing horizontal desks in remaining spaces
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a horizontal desk
                        if col + 1 < x and matrix[row][col + 1] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row, col + 1)]):
                                matrix[row][col] = 'X'
                                matrix[row][col + 1] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
    return desks_placed, matrix


def has_adjacent_desk(matrix, i, j, x, y, desk_cells):
    """Check if any adjacent cells (including diagonally) have a desk."""
    for ci, cj in desk_cells:
        for ni in range(ci - 1, ci + 2):
            for nj in range(cj - 1, cj + 2):
                if (ni, nj) == (ci, cj):
                    continue
                if 0 <= ni < y and 0 <= nj < x:
                    if matrix[ni][nj] == 'X':
                        return True
    return False

def format_output(room_results: List[str]) -> str:
    """Format the results by joining the room matrices."""
    return '\n\n'.join(room_results)


if __name__ == '__main__':
    import os
    from pathlib import Path

    input_location = Path("../Inputs/level5")
    output_location = Path("../Outputs/level5")

    # Load input files
    input_files = ["/home/jd/git/uni/CCC/CCC/Challenge 2024/Inputs/level5/level5_1.in"] # load_inputs(input_location)

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
