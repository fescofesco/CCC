from dataclasses import dataclass
from typing import List, Tuple


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
    results = []

    for room_info in room_infos:
        x, y, desks_to_place = room_info.x, room_info.y, room_info.desks_to_place

        # Simulate both orientations
        desks_h, matrix_h = simulate_horizontal_placement(x, y)
        desks_v, matrix_v = simulate_vertical_placement(x, y)

        # Choose the orientation that can place the required number of desks
        # If both can, choose the one with the higher total capacity
        if desks_h >= desks_to_place and desks_h >= desks_v:
            desks_placed = desks_h
            matrix = matrix_h
        elif desks_v >= desks_to_place:
            desks_placed = desks_v
            matrix = matrix_v
        else:
            # Neither orientation can meet the requirement
            # Choose the one with the higher total capacity
            if desks_h >= desks_v:
                desks_placed = desks_h
                matrix = matrix_h
            else:
                desks_placed = desks_v
                matrix = matrix_v

        # If after placement, we still need more desks, attempt to place additional desks
        if desks_placed < desks_to_place:
            desks_needed = desks_to_place - desks_placed
            desks_placed += place_additional_desks(matrix, desks_needed, x, y)

        # If still not enough desks, handle accordingly
        if desks_placed < desks_to_place:
            print(
                f"Warning: Could not place all desks in room {x}x{y}. Placed {desks_placed} desks out of {desks_to_place}.")

        # Convert the matrix to the required output format
        matrix_output = '\n'.join(''.join(row) for row in matrix)
        results.append(matrix_output)

    return results


def simulate_horizontal_placement(x: int, y: int) -> Tuple[int, List[List[str]]]:
    matrix = [['.'] * x for _ in range(y)]
    desks_placed = 0
    block_w, block_h = 3, 2
    desk_pos = [(0, 0), (0, 1)]  # Desk occupies (i, j) and (i, j+1)

    for i in range(0, y):
        for j in range(0, x):
            if matrix[i][j] != '.':
                continue

            # Try to place horizontally
            if j + 1 < x and matrix[i][j + 1] == '.':
                # Check adjacency
                if not has_adjacent_desk(matrix, x, y, [(i, j), (i, j + 1)]):
                    matrix[i][j] = 'X'
                    matrix[i][j + 1] = 'X'
                    desks_placed += 1
                    # Skip the next two columns to maintain the 2x3 block pattern
                    j += 2
            # Move to next possible position

    return desks_placed, matrix


def simulate_vertical_placement(x: int, y: int) -> Tuple[int, List[List[str]]]:
    matrix = [['.'] * x for _ in range(y)]
    desks_placed = 0
    block_w, block_h = 2, 3
    desk_pos = [(0, 0), (1, 0)]  # Desk occupies (i, j) and (i+1, j)

    for j in range(0, x):
        for i in range(0, y):
            if matrix[i][j] != '.':
                continue

            # Try to place vertically
            if i + 1 < y and matrix[i + 1][j] == '.':
                # Check adjacency
                if not has_adjacent_desk(matrix, x, y, [(i, j), (i + 1, j)]):
                    matrix[i][j] = 'X'
                    matrix[i + 1][j] = 'X'
                    desks_placed += 1
                    # Skip the next two rows to maintain the 3x2 block pattern
                    i += 2
            # Move to next possible position

    return desks_placed, matrix


def has_adjacent_desk(matrix, x, y, desk_cells):
    """Check if any adjacent cells (including diagonals) have a desk."""
    for ci, cj in desk_cells:
        for ni in range(ci - 1, ci + 2):
            for nj in range(cj - 1, cj + 2):
                if (ni, nj) in desk_cells:
                    continue
                if 0 <= ni < y and 0 <= nj < x:
                    if matrix[ni][nj] == 'X':
                        return True
    return False


def place_additional_desks(matrix, desks_needed, x, y):
    """Attempt to place additional desks where possible."""
    desks_placed = 0
    for i in range(y):
        for j in range(x):
            if desks_placed >= desks_needed:
                return desks_placed
            if matrix[i][j] == '.':
                # Try horizontal placement
                if j + 1 < x and matrix[i][j + 1] == '.':
                    if not has_adjacent_desk(matrix, x, y, [(i, j), (i, j + 1)]):
                        matrix[i][j] = 'X'
                        matrix[i][j + 1] = 'X'
                        desks_placed += 1
                        continue  # Move to next position
                # Try vertical placement
                if i + 1 < y and matrix[i + 1][j] == '.':
                    if not has_adjacent_desk(matrix, x, y, [(i, j), (i + 1, j)]):
                        matrix[i][j] = 'X'
                        matrix[i + 1][j] = 'X'
                        desks_placed += 1
    return desks_placed


def format_output(room_results: List[str]) -> str:
    """Format the results by joining the room matrices."""
    return '\n\n'.join(room_results)


if __name__ == '__main__':
    import os
    from pathlib import Path

    # input_location = Path("../Inputs/level5")
    output_location = Path("../Outputs/level5")

    # Load input files
    input_files = ["/home/jd/git/uni/CCC/CCC/Challenge 2024/Inputs/level5/level5_1.in"]  # load_inputs(input_location)

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
