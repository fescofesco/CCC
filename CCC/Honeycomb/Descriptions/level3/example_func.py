#%%
def find_W_path(grid_string, w_row, w_col):
    # Convert the grid string into a 2D grid
    grid = [row.split('-') for row in grid_string.strip().split("\n")]

    # Hexagonal neighbors for odd and even rows
    even_neighbors = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
    odd_neighbors = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]

    # Function to check if a position is valid (within bounds and not an obstacle)
    def is_valid(r, c):
        return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != 'X'

    # Function to try moving in a specific direction (dr, dc)
    def try_direction(dr, dc):
        row, col = w_row, w_col
        while is_valid(row + dr, col + dc):
            row += dr
            col += dc
            if row == 0 or col == 0 or row == len(grid) - 1 or col == len(grid[0]) - 1:
                return "FREE"
        return "TRAPPED"
    
    # Try moving in a straight line from 'W'
    for r, c in [(w_row, w_col)]:
        neighbors = even_neighbors if r % 2 == 0 else odd_neighbors

        # Try each neighbor direction, continue in a straight line
        for dr, dc in neighbors:
            if is_valid(r + dr, c + dc):
                # Try moving in that direction
                return try_direction(dr, dc)
    
    return "TRAPPED"

# Sample grid
grid_string = """
X-X-O-O-X-O-X-O-X-X-
-O-O-O-X-O-O-O-O-X-O
O-X-O-X-O-O-X-O-O-X-
-X-O-O-O-O-X-O-X-O-O
X-X-O-O-O-O-O-O-X-X-
-X-X-O-O-O-X-O-O-O-X
X-W-X-O-X-O-X-O-O-O-
-X-X-O-O-O-O-O-X-O-O
"""

grid_string = """
X-X-O-O-X-O-X-O-X-X-
-O-O-O-X-O-O-O-O-X-O
O-X-O-X-O-O-X-O-O-X-
-X-O-O-O-O-X-O-X-O-O
X-X-O-O-O-O-O-O-X-X-
-X-X-O-O-O-X-O-O-O-X
X-W-X-O-X-O-X-O-O-O-
-X-X-O-O-O-O-O-X-O-O
"""

# Find the position of the 'W' in the grid
def find_w_position(grid_string, verbose:int=0):
    w_row, w_col = None, None
    for r, row in enumerate(grid_string.strip().split("\n")):
        for c, cell in enumerate(row.split('-')):
            if cell == 'W':
                w_row, w_col = r, c
                if verbose >1:
                    print("Starting position of W:", w_row, w_col)
                break
        if w_row is not None and w_col is not None:
            break
    return w_row,w_col

w_row, w_col = find_w_position(grid_string)

# Call the function with the found coordinates of W
result = find_W_path(grid_string, w_row, w_col)
print(result)


# %%
