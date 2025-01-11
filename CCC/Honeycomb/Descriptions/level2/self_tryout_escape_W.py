#%%
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
grid = [row.split('-') for row in grid_string.strip().split("\n")]

print(grid)


# Convert the string into a 2D matrix (list of lists)
def find_W_neighbours(grid_string, w_row, w_col):
    # grid = [row.split('-') for row in grid_string.strip().split("\n")]
    grid = [row.split('-') for row in grid_string.strip().split("\n")]
    grid = [row.split('-') for row in grid_string.strip().split("\n")]

    # Hexagonal neighbors offsets
    # For odd and even rows, neighbors are slightly different
    
    running = True
    free = False

        
    for dir in ["nw", "ne","e","se","sw","w"]:
        row_now =w_row 
        column_now = w_col

        while running:
            if dir == "nw":
                next_cell = (-1,-1) if row_now %2 ==0 else (-1,0) #even dann odd 
            if dir == "ne":
                next_cell = (-1,0) if row_now%2 ==0 else (-1,1)
            if dir == "e":
                next_cell = (0,1)
            if dir == "se":
                next_cell = (-1,0) if row_now%2 == 0 else (-1,1)
            if dir == "sw":
                next_cell = (-1,-1) if row_now %2 == 0 else (-1,0)
            if dir == "w":
                next_cell = (0,-1) 
            
            nr, nc = row_now +(next_cell)[0],  column_now +  (next_cell)[1] 

            if grid[nr][nc] == 'O':  # Check for empty cell
                print(grid[nr][nc])
                print("nr",nr," nc",nc)
                row_now = nr
                column_now = nc

            if grid[nr][nc] == 'X':
                result = "TRAPPED"
                running = False  
            if [nr] == grid.len()[0] or [nc] == grid.len()[1] or [nr] ==0 or [nc]==0:
                result = "FREE"
                free = True
                running = False
        
    return free

# Find the position of the 'W' in the grid

for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        if cell == 'W':
            w_row, w_col = r, c
            print("hier schaut er nach", w_row, w_col)
            break

result_escape = find_W_neighbours(grid, w_row, w_col)
print(result_escape)