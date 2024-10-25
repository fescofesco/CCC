from dataclasses import dataclass
from typing import List


def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory."""
    input_files = []
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files


@dataclass
class RoomDeskInfo:
    x: int
    y: int
    desk_count: int
    id: int


def parse_input(input_string):
    lines = input_string.strip().split('\n')
    N = int(lines[0])  # Number of rooms

    room_infos = []
    for i in range(1, N + 1):
        x, y, desk_count = map(int, lines[i].split())
        room_infos.append(RoomDeskInfo(x, y, desk_count, i))
    return room_infos



def format_output(desk_counts):
    return '\n'.join(map(str, desk_counts))


def provide_room_id_matrix(room_infos: List[RoomDeskInfo]) -> str:
    room_id_matrix = ""

    room_count = 0
    for room_info in room_infos:
        for i in range(3):
            room_id_matrix += f"{room_info.id} "

        if room_count == room_infos.x / 3:
            room_id_matrix += "\n"
        room_count += 1
    return room_id_matrix

if __name__ == '__main__':
    import os
    from pathlib import Path

    input_location = Path("../Inputs/level2")
    output_location = Path("../Outputs/level2")
    input_files = load_inputs(input_location)
    for f_p in input_files:
        with open(f_p, "r") as file:
            input_string = file.read()
        rooms = parse_input(input_string)
        room_result = provide_room_id_matrix(rooms)
        out_fp = output_location / (Path(f_p).stem + ".out")
        with open(out_fp, "w") as file:
            file.write(room_result)
