from optimize import max_desks_in_room

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
    with open("/home/jd/git/uni/CCC/CCC/Challenge 2024/Inputs/level1/level1_1.in", "r") as file:
        input_string = file.read()
    rooms = parse_input(input_string)
    desk_counts = calculate_desks(rooms)
    output_string = format_output(desk_counts)
    with open("/home/jd/git/uni/CCC/CCC/Challenge 2024/level1/level1.out", "w") as file:
        file.write(output_string)
