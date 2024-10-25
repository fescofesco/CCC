def max_desks_in_room(x, y):
    # Desk dimensions
    desk_width = 3
    desk_height = 1

    # Maximum desks that can fit along the width and height of the room
    desks_in_width = x // desk_width
    desks_in_height = y // desk_height

    # Total desks that can fit in the room
    total_desks = desks_in_width * desks_in_height

    return total_desks

# Example usage with arbitrary room dimensions
rooms = [(6, 5), (9, 8), (6, 7)]
desk_counts = [max_desks_in_room(x, y) for x, y in rooms]

print("Maximum number of desks for each room:", desk_counts)
