#%%
from dataclasses import dataclass
from typing import List

from lvl4_freeortrapped import freeOrTrapped, find_w_position
from chat_lvl5_freeortrapped import evaluate_and_place_obstacles,print_hexagonal_grid

def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory."""
    print(f"Looking for files in: {os.path.abspath(location)}")
    input_files = []
    print(os.listdir(location))
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files



def lvl2_parse_combs(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().strip().split("\n")
    
    # First line gives the number of combs
    num_combs = int(lines[0].strip())
    
    # Split the remaining lines into combs using empty lines as delimiters
    comb_lines = lines[1:]  # Skip the first line
    combs = []
    current_comb = []

    for line in comb_lines:
        if line.strip():  # Non-empty line
            current_comb.append(line.split('-'))
        else:  # Empty line separates combs
            if current_comb:  # Add the current comb if not empty
                combs.append(current_comb)
                current_comb = []
    
    # Add the last comb if any
    if current_comb:
        combs.append(current_comb)

    return num_combs, combs


def lvl3_parse_combs(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().strip().split("\n")
    
    # First line gives the number of combs
    num_combs = int(lines[0].strip())
    
    # Split the remaining lines into combs using empty lines as delimiters
    comb_lines = lines[1:]  # Skip the first line
    combs = []
    current_comb = []

    for line in comb_lines:
        if line.strip():  # Non-empty line
            current_comb.append(line.split('-'))
        else:  # Empty line separates combs
            if current_comb:  # Add the current comb if not empty
                combs.append(current_comb)
                current_comb = []
    
    # Add the last comb if any
    if current_comb:
        combs.append(current_comb)

    return num_combs, combs




def find_W_neighbours(combs):
    results = []

    for grid_string in combs:
        # Convert the comb (grid) into a 2D matrix
        grid = [row for row in grid_string]

        # Hexagonal neighbors offsets
        even_neighbors = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        odd_neighbors = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]

        def count_empty_neighbors(grid, w_row, w_col):
            # Choose the correct neighbor offsets based on the row index
            neighbors = even_neighbors if w_row % 2 == 0 else odd_neighbors
            count = 0
            for dr, dc in neighbors:
                nr, nc = w_row + dr, w_col + dc

                # Check if neighbor is within grid boundaries
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    if grid[nr][nc] == 'O':  # Check for empty cell
                        count += 1
            return count

        # Find the position of the 'W' in the grid
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == 'W':
                    w_row, w_col = r, c
                    break

        # Count the empty neighbors around 'W'
        empty_neighbors = count_empty_neighbors(grid, w_row, w_col)
        results.append(empty_neighbors)

    return results

def lvl1_parse_input(input_string: str) -> int:

    return combs


def lvl2_count_empty_cells(input_string: str): 

    empty_cells = 1
    return empty_cells

def lvl5_parse_combs(file_path, verbose=0):
    with open(file_path, 'r') as file:
        lines = file.read().strip().split("\n")
    
    if verbose > 3:
        print("File content lines:", lines)
    
    # First line gives the number of grids
    num_grids = int(lines[0].strip())
    grids = []
    num_obstacles_list = []

    current_index = 1  # Start processing after the number of grids line
    while current_index < len(lines):
        # Skip empty lines
        if lines[current_index].strip() == "":
            current_index += 1
            continue

        # Read the number of obstacles for this grid
        num_obstacles = int(lines[current_index].strip())
        num_obstacles_list.append(num_obstacles)
        current_index += 1

        # Read the grid
        grid = []
        while current_index < len(lines) and lines[current_index].strip() != "":
            grid.append(lines[current_index].split('-'))
            # grid.append(lines[current_index].strip())
            current_index += 1
        grids.append(grid)
        if verbose >2:
            print("type(grid)", type(grid))
        if verbose > 3:
            print(f"Processed grid with {num_obstacles} obstacles:")
            for row in grid:
                print(row)
    
    if verbose > 2:
        print("file_path:", file_path)
        print(f"Total grids: {num_grids}")
        print("Number of obstacles for each grid:", num_obstacles_list)
    
    return num_grids, num_obstacles_list, grids

def format_output(num_combs):
    output = "\n".join(str(count) for count in results)
    return output

if __name__ == '__main__':
 
    import os
    from pathlib import Path

    level3 = False

    level4 = False
    level5 = True

    if level4 == True:
        input_location = Path(r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Inputs\level4")
        output_location = Path(r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Outputs\level4")    
    if level5 == True:
        input_location = Path(r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Inputs\level5")
        output_location = Path(r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Outputs\level5")

        # Format the grid as required
    def format_grid(grid):
        return "\n".join("-".join(row) for row in grid)


    # Load input files
    input_files = load_inputs(input_location)
    verbose = 0

    for f_p in input_files:
        if f_p != r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Inputs\level5\level5_5.in":
            continue

        print(f"Processing: {f_p}")
        results = []

        if level3:
            num_combs, combs = lvl3_parse_combs(f_p)
        
        if level5:
            verbose = 1
            num_grids, num_obstacles, grids = lvl5_parse_combs(f_p, verbose=verbose)
            # if verbose >2: print(f"num grids :{num_grids}  num_obstacles {num_obstacles} grids {grids}")
            results.append(str(len(num_obstacles)))
            results.append("")  # Empty line for separation

        for grid, num_obstacle in zip(grids, num_obstacles):
            # Find the position of 'W'
            w_row, w_col = find_w_position(grid)
            if w_row is None or w_col is None:
                raise ValueError("No 'W' found in the grid.")
            
            # Determine if 'W' is free or trapped after placing obstacles
            try:
                resulting_grid = evaluate_and_place_obstacles(grid, num_obstacles=num_obstacle, verbose=1)
                if resulting_grid is None:
                    print("resulting_grid is None")
                    print_hexagonal_grid(grid)
                
            except ValueError as e:
                result = str(e)  # Capture the error message if trapping fails
                # print_hexagonal_grid(grid)  
            # Append the result along with the number of obstacles used
            # results.append(str(num_obstacle))
             # Append formatted result
            # results.append(str(num_obstacle))  # Obstacle count
            results.append(format_grid(resulting_grid))  # Formatted grid
            results.append("")  # Empty line for separation
                    # Format output
        if verbose >3:
            print("results", results)
        formatted_output = "\n".join(results)

        output_location.mkdir(parents=True, exist_ok=True)
        out_fp = output_location / (Path(f_p).stem + ".out")
        with open(out_fp, "w") as file:
            file.write(formatted_output)
        print(out_fp, "saved.")
        