#%%
from dataclasses import dataclass
from typing import List

from lvl3_freeOrTrapped import freeOrTrapped, find_w_position

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

def format_output(num_combs):
    output = "\n".join(str(count) for count in results)
    return output

if __name__ == '__main__':
    import os
    from pathlib import Path

    import os
    from pathlib import Path

    input_location = Path(r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Inputs\level3")
    output_location = Path(r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Outputs\level3")

    # Load input files
    input_files = load_inputs(input_location)
    level3 = True
    verbose = 0

    for f_p in input_files:
        num_combs, combs = lvl3_parse_combs(f_p)

        results = []
        for grid in combs:
            # Find the position of 'W'
            w_row, w_col = find_w_position(grid, verbose=verbose)

            # Determine if 'W' is free or trapped
            result = freeOrTrapped(grid, w_row, w_col, verbose=verbose)
            results.append(result)

        # Format output
        formatted_output = "\n".join(results)

        output_location.mkdir(parents=True, exist_ok=True)
        out_fp = output_location / (Path(f_p).stem + ".out")
        with open(out_fp, "w") as file:
            file.write(formatted_output)
        print(out_fp, "saved.")
        

    # input_location = Path("././Inputs/level3") 
    # input_location = Path(r"C:\Users\felix\Documents\CCC\CCC\Honeycomb\Inputs\level3")
    #                       #Path("./././Inputs/level3")
    # output_location = Path("./././Outputs/level3")

    # # Load input files
    # input_files = load_inputs(input_location)
    # # input_files = [Path("../../Inputs/level2/level2_example.in")]

    # # input_files = load_inputs(input_location)

    # level1 = False
    # level2 = False
    # level3 = True
  
    # for f_p in input_files:
    #     if level1:
    #          with open(f_p, "r") as file:
    #             input_string = file.read()
    #             # Parse input
    #             num_combs = lvl1_parse_input(input_string)
    #             output_unformated = num_combs
        
    #     if level2:
    #         num_combs, combs = lvl2_parse_combs(f_p)
    #         results = find_W_neighbours(combs)
    #         formatted_output = format_output(results) 

    #     if level3:
    #         num_combs, combs = lvl3_parse_combs(f_p)   
            
    #         grid_string = combs[0]
    #         print("grid_string:", grid_string)
    #         w_row, w_col = find_w_position(grid_string, verbose=1)
    #         print(w_row, w_col)
    #         result = freeOrTrapped(grid_string, w_row, w_col)
    #         print(result)    

    #     formatted_output = format_output(output_unformated)

    #     output_location.mkdir(parents=True, exist_ok=True)
    #     # Write the output to the corresponding file
    #     out_fp = output_location / (Path(f_p).stem + ".out")
    #     with open(out_fp, "w") as file:
    #         file.write(formatted_output)
