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
