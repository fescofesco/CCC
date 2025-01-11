

# Input grid as a string
grid_string = """
X-X-O-O-X-O-X-O-X-X-
-O-O-O-X-O-O-O-O-X-O
O-X-O-X-O-O-X-O-O-X-
-X-O-O-O-O-X-O-X-O-O
X-X-O-O-O-O-O-O-X-X-
-X-O-O-O-O-X-O-O-O-X
O-W-X-O-X-O-X-O-O-O-
-X-O-O-O-O-O-O-X-O-O
"""

grid_string = """
X-X-O-O-X-O-X-O-X-X-
-O-O-O-O-O-O-O-O-X-O
O-X-O-O-O-O-X-O-O-X-
-X-O-O-O-O-X-O-X-O-O
X-X-O-O-O-O-O-O-X-X-
-X-O-O-O-O-X-O-O-O-X
X-W-O-O-X-O-X-O-O-O-
-X-X-O-O-O-O-O-X-O-O
"""
# Convert the string into a 2D matrix (list of lists)
grid = [row.split('-') for row in grid_string.strip().split("\n")]


print(grid)

def find_W_neighbours(grid, w_row, w_col):
    # No need to split the grid again, it's already a 2D list.
    # Hexagonal neighbors offsets
    free = False
    
    
    for dir in ["nw"]:#["nw", "ne", "e", "se", "sw", "w"]:
        print("dir:", dir)
        running = True
        print("starting pos ",w_row, w_col, grid[w_row][w_col])
        row_now = w_row
        column_now = w_col

        while running:
            if dir == "nw":
                # next_cell = (-1, -1) if row_now % 2 == 0 else (-1, 0)
                next_cell = (-1, -1) if row_now % 2 == 0 else (-1, 0)
            if dir == "ne":
                next_cell = (-1, 0) if row_now % 2 == 0 else (-1, 1)
            if dir == "e":
                next_cell = (0, 1)
            if dir == "se":
                next_cell = (1, 0) if row_now % 2 == 0 else (1, 1)
            if dir == "sw":
                next_cell = (1, -1) if row_now % 2 == 0 else (1, 0)
            if dir == "w":
                next_cell = (0, -1)
            
            nr, nc = row_now + next_cell[0], column_now + next_cell[1]
          
            # if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):  # Check if within bounds
            if nr == -1 or nc == -1 or nr == len(grid)  or nc == len(grid[0]) :
                print("free at ",nr, nc)
                result = "FREE"
                free = True
                running = False
            elif grid[nr][nc] == 'O':  # Check for empty cell
                print(grid[nr][nc])
                print("nr", nr, "nc", nc)
                row_now = nr
                column_now = nc
            elif grid[nr][nc] == '':  # Check for empty cell
                free = True
                running = False
            elif grid[nr][nc] == 'X':  # Blocked path
                print([nr],[nc],"Trapped")
                result = "TRAPPED"
                running = False  
            else:
                result = "TRAPPED"
                running = False

    return "FREE" if free else "TRAPPED"


# Find the position of the 'W' in the grid
for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        if cell == 'W':
            w_row, w_col = r, c  
            print("Starting position of W:", w_row, w_col)
            break

# Call the function with the found coordinates of W
result_escape = find_W_neighbours(grid, w_row, w_col)
print(result_escape)
