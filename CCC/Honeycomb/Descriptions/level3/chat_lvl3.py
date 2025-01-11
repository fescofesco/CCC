#%%
def print_hexagonal_grid(grid):
    # Handle both grid_list and grid_string inputs
    if isinstance(grid, str):
        # Strip leading/trailing spaces from each line and split into a list of lists
        grid = [row.strip().split('-') for row in grid.strip().split("\n")]

    # Format the grid as a hexagonal layout
    formatted_grid = "\n".join(
        "-".join(row)
        for r, row in enumerate(grid)
    )
    print("\n" + formatted_grid + "\n")

def freeOrTrapped(grid, w_row, w_col, verbose: int = 0):
    if isinstance(grid, str):
        grid = [row.split('-') for row in grid.strip().split("\n")]

    def get_directions(row):
        """
        Returns the directional offsets for a hexagonal grid.
        Accounts for the parity of the row (even or odd).
        """
        top_left = (-1, -1) if row % 2 == 1 else (-1, 0)
        top_right = (-1, 0) if row % 2 == 1 else (-1, 1)
        bottom_left = (1, -1) if row % 2 == 1 else (1, 0)
        bottom_right = (1, 0) if row % 2 == 1 else (1, 1)
        left = (0, -1)
        right = (0, 1)
        return {
            "top_left": top_left,
            "top_right": top_right,
            "bottom_left": bottom_left,
            "bottom_right": bottom_right,
            "left": left,
            "right": right,
        }


    def is_valid(r, c, verbose=0):
        within_bounds = 0 <= r < len(grid) and 0 <= c < len(grid[0])
        is_not_obstacle = grid[r][c] != 'X' if within_bounds else False
        if verbose > 1:
            print(f"Checking cell ({r}, {c}): within_bounds={within_bounds}, is_not_obstacle={is_not_obstacle}")
        return within_bounds and is_not_obstacle

    def is_edge(r, c):
        return r == 0 or c == 0 or r == len(grid) - 1 or c == len(grid[0]) - 1
    
    def get_next_position(row, col, dr, dc):
        next_row = row + dr
        next_col = col + dc
        if row % 2 == 0:
            next_col += 1
        return next_row, next_col


    def try_direction(w_row, w_col, direction_name, grid, verbose=0):
        """
        Follows the given direction until reaching the edge of the grid or an obstacle.
        Returns 'FREE' if the edge is reached, or 'TRAPPED' if blocked by an obstacle.
        """
        row, col = w_row, w_col

        while True:
            directions = get_directions(row)
            if verbose >2: print("directions",directions)
            if verbose > 2 : print("direction_name",direction_name[0])
            dr, dc = directions[direction_name[0]]

        # while True:
        #     dr, dc = get_directions(row, direction_name)
        #     # Calculate the next position
            next_row = row + dr
            next_col = col + dc

            # Check if the next position is valid
            if next_row < 0 or next_row >= len(grid) or next_col < 0 or next_col >= len(grid[0]):
                if verbose > 0:
                    print(f"Reached the edge at ({row}, {col}). Returning 'FREE'.")
                return "FREE"

            if grid[next_row][next_col] == 'X':  # Encounter an obstacle
                if verbose > 0:
                    print(f"Blocked at ({next_row}, {next_col}). Returning 'TRAPPED'.")
                return "TRAPPED"

            # Move to the next position
            row, col = next_row, next_col
            if verbose > 1:
                print(f"Moved to ({row}, {col}).")

        

    # # Try all directions
    # initial_directions = get_directions(w_row)
    # directions_to_check = ["top_left", "top_right", "bottom_left", "bottom_right", "left", "right"]
    # for direction in directions_to_check:
    #     # dr, dc = initial_directions[directions_to_check.index(direction)]
    #     dr, dc = initial_directions[direction]  # Use the string 'direction' to access the dictionary
    #     result = try_direction(dr, dc, verbose)
    #     if result == "FREE":
    #         return "FREE"

    directions = get_directions(w_row)
    for direction_name in directions.items():
        if verbose > 0:
            print(f"Trying direction: {direction_name[0]}")
        result = try_direction(w_row, w_col, direction_name, grid, verbose)
        if result == "FREE":
            return "FREE"


    return "TRAPPED"


# Find the position of the 'W' in the grid
def find_w_position(grid, verbose=0):
    w_row, w_col = None, None

    # Handle both grid_list and grid_string inputs
    if isinstance(grid, str):
        grid = [row.split('-') for row in grid.strip().split("\n")]

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'W':
                w_row, w_col = r, c
                if verbose > 1:
                    print("Starting position of W:", w_row, w_col)
                    print("starting at value",cell)
                break
        if w_row is not None and w_col is not None:
            break
    return w_row, w_col

if __name__ == "__main__":
    # Example with grid string
    grid_string = """
    X-X-O-O-X-O-X-O-X-X-
    -O-O-O-X-O-O-O-O-X-O
    O-X-O-X-O-O-X-O-O-X-
    -X-O-O-O-O-X-O-X-O-O
    X-X-O-X-O-O-O-O-X-X-
    -X-X-O-O-O-X-O-O-O-X
    O-W-X-O-X-O-X-O-O-O-
    -X-X-O-O-O-O-O-X-O-O
    """

    grid_string = """
    O-X-X-O-X-
    -O-O-O-X-O
    X-O-W-O-O-
    -O-X-X-X-X
    O-X-X-O-O-

    """
    # Example with grid list
    grid_list = [
        ['X', 'X', 'X', 'O', 'X', 'O', 'X', 'O', 'O', 'X'],
        ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['X', 'X', 'O', 'W', 'O', 'O', 'O', 'X', 'O', 'X'],
        ['X', 'X', 'O', 'X', 'X', 'X', 'X', 'O', 'O', 'O'],
        ['X', 'X', 'O', 'O', 'X', 'O', 'X', 'X', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'X', 'X', 'X', 'O', 'O'],
        ['O', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O', 'O'],
        ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'X', 'O', 'X']
    ]

    grid_string = """
    X-O-O-O-X-
    -O-X-X-X-X
    O-O-O-O-X-
    -X-W-O-O-X
    O-X-X-O-X-
    """
    grid_string = """
    X-X-X-O-O-O-O-O-X-O-
    -O-X-O-O-O-X-X-O-O-X
    O-O-X-O-O-O-O-X-O-X-
    -O-O-O-X-O-O-X-O-X-O
    O-O-X-X-O-O-O-X-O-X-
    -O-O-O-X-O-O-O-X-O-O
    O-O-X-O-O-X-W-O-X-X-
    -O-O-O-X-X-X-X-X-O-O
    """
    # # Test with grid_string
    w_row, w_col = find_w_position(grid_string, verbose=2)
    print("Position in string:", w_row, w_col)
    result = freeOrTrapped(grid_string, w_row, w_col, verbose = 3)
    print("Result (string):", result)

 
