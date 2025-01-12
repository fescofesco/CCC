from optimize import max_desks_in_room


def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory."""
    input_files = []
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files


def parse_input(input_string):
    lines = input_string.strip().split('\n')
    N = int(lines[0])  # Number of rooms
    rooms = []

    # Parse each room dimension
    for i in range(1, N + 1):
        x, y = map(int, lines[i].split())
        rooms.append((x, y))

    return rooms




def calculate_desks(rooms):
    desk_counts = [max_desks_in_room(x, y) for x, y in rooms]
    return desk_counts

def format_output(desk_counts):
    return '\n'.join(map(str, desk_counts))

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
        desk_counts = calculate_desks(rooms)
        
        output_string = format_output(desk_counts)
        out_fp = output_location / (Path(f_p).stem + ".out")
        with open(out_fp, "w") as file:
            file.write(output_string)
