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


from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class RoomDeskInfo:
    x: int  # Room length (x-axis)
    y: int  # Room height (y-axis)
    desks_to_place: int  # Fixed number of desks to place


def provide_room_matrix(room_infos: List[RoomDeskInfo]) -> List[str]:
    results = []

    for room_info in room_infos:
        x, y, desks_to_place = room_info.x, room_info.y, room_info.desks_to_place
        best_desks = 0
        best_matrix = None
        solution_found = False

        # Try all possible starting offsets and orientations
        for start_i in range(2):
            for start_j in range(2):
                for orientation in ['H', 'V']:
                    matrix = [['.'] * x for _ in range(y)]
                    desks_placed = 0
                    unavailable = [[False] * x for _ in range(y)]
                    for i in range(start_i, y):
                        for j in range(start_j, x):
                            if desks_placed >= desks_to_place:
                                solution_found = True
                                break
                            if unavailable[i][j]:
                                continue
                            placed = False
                            if orientation == 'H' and j + 1 < x and not unavailable[i][j + 1]:
                                if not has_adjacent_desk(unavailable, i, j, x, y, [(i, j), (i, j + 1)]):
                                    # Place the desk
                                    matrix[i][j] = 'X'
                                    matrix[i][j + 1] = 'X'
                                    desks_placed += 1
                                    mark_unavailable(unavailable, i, j, x, y, [(i, j), (i, j + 1)])
                                    placed = True
                            if not placed and orientation == 'V' and i + 1 < y and not unavailable[i + 1][j]:
                                if not has_adjacent_desk(unavailable, i, j, x, y, [(i, j), (i + 1, j)]):
                                    # Place the desk
                                    matrix[i][j] = 'X'
                                    matrix[i + 1][j] = 'X'
                                    desks_placed += 1
                                    mark_unavailable(unavailable, i, j, x, y, [(i, j), (i + 1, j)])
                                    placed = True
                        if solution_found:
                            break
                    # Check if we've found a solution
                    if desks_placed >= desks_to_place:
                        best_desks = desks_placed
                        best_matrix = matrix
                        solution_found = True
                        break  # Break out of orientation loop
                    else:
                        # Keep the best result so far
                        if desks_placed > best_desks:
                            best_desks = desks_placed
                            best_matrix = matrix
                if solution_found:
                    break  # Break out of start_j loop
            if solution_found:
                break  # Break out of start_i loop

        if best_matrix is None:
            print(f"Could not place any desks in room {x}x{y}.")
            matrix = [['.'] * x for _ in range(y)]
        else:
            matrix = best_matrix
            if best_desks < desks_to_place:
                print(
                    f"Warning: Could not place all desks in room {x}x{y}. Placed {best_desks} desks out of {desks_to_place}.")
        # Convert the matrix to the required output format
        matrix_output = '\n'.join(''.join(row) for row in matrix)
        results.append(matrix_output)
    return results


def has_adjacent_desk(unavailable, i, j, x, y, desk_cells):
    """Check if any adjacent cells (including diagonally) are unavailable."""
    for ci, cj in desk_cells:
        for ni in range(ci - 1, ci + 2):
            for nj in range(cj - 1, cj + 2):
                if (ni, nj) in desk_cells:
                    continue
                if 0 <= ni < y and 0 <= nj < x:
                    if unavailable[ni][nj]:
                        return True
    return False


def mark_unavailable(unavailable, i, j, x, y, desk_cells):
    """Mark the cells occupied by the desk and all adjacent cells as unavailable."""
    # Mark desk cells
    for ci, cj in desk_cells:
        unavailable[ci][cj] = True
    # Mark adjacent cells
    for ci, cj in desk_cells:
        for ni in range(ci - 1, ci + 2):
            for nj in range(cj - 1, cj + 2):
                if 0 <= ni < y and 0 <= nj < x:
                    unavailable[ni][nj] = True


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
