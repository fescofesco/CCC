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

        
        horizontal_value = math.floor(x/3) * math.floor((y+1)/2)
        vertical_value = math.floor((x+1)/2) * math.floor((y)/3)
        
        start_horizontally = horizontal_value > vertical_value

        bigger_dim = x if start_horizontally else y
        # smaller_dim = y if start_horizontally else x


        current_ind = 0
        while current_ind < bigger_dim - 3:
            for col in range(0, bigger_dim, 2):
                for row in range(current_ind, current_ind+2):
                    if start_horizontally:
                        matrix[row][col] = 'X'
                    else:
                        matrix[col][row] = 'X'

                desks_placed += 1
                if desks_placed >= desk_count:
                    break
            current_ind += 3

        # if desks_placed < desk_count:
        #     rows_left = smaller_dim - current_ind
        #     if rows_left > 0:
        #         current_ind = 0
        #         while desks_placed < desk_count:

        #             row = smaller_dim - 1
        #             for col in range(current_ind, current_ind+2):
        #                 if not star_horizontally:
        #                     matrix[col][row] = 'X'
        #                 else:
        #                     matrix[row][col] = 'X'
        #             current_ind += 3
        #             desks_placed += 1

        matrix_output = '\n'.join(''.join(row) for row in matrix)
        results.append(matrix_output)

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