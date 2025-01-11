# Input grid as a string
grid_string = """
X-X-O-O-X-O-X-O-X-X-
-O-O-O-X-O-O-O-O-X-O
O-X-O-X-O-O-X-O-O-X-
-X-O-O-O-O-X-O-X-O-O
X-X-O-O-O-O-O-O-X-X-
-X-O-O-O-O-X-O-O-O-X
O-W-O-O-X-O-X-O-O-O-
-O-O-O-O-O-O-O-X-O-O
"""

# Convert the string into a 2D matrix (list of lists)
def find_W_neighbours(grid_string):
    grid = [row.split('-') for row in grid_string.strip().split("\n")]

    # Hexagonal neighbors offsets
    # For odd and even rows, neighbors are slightly different

    even_neighbors = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
    odd_neighbors = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]

    def count_empty_neighbors(grid, w_row, w_col):
    # Choose the correct neighbor offsets based on the row index
        neighbors = even_neighbors if w_row % 2 == 0 else odd_neighbors
        count = 0
        for dr, dc in neighbors:
            nr, nc = w_row + dr, w_col + dc
    

        # Check if neighbor is within grid boundaries
        # if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
        #     if grid[nr][nc] == 'O':  # Check for empty cell
        #         print(grid[nr][nc])
        #         print("nr",nr," nc",nc)
        #         count += 1
        # if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] == 'O':  # Check for empty cell
                print(grid[nr][nc])
                print("nr",nr," nc",nc)
                count += 1
        return count

# Find the position of the 'W' in the grid
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'W':
                w_row, w_col = r, c
                print("hier schaut er nach", w_row, w_col)
                break
   
    empty_neighbors = count_empty_neighbors(grid, w_row, w_col)

    return empty_neighbors
