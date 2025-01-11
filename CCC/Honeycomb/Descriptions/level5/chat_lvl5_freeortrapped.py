#%%
from collections import deque
from itertools import combinations, product
from copy import deepcopy

def format_grid(grid):
    """
    Format the grid where every O and X is separated by '-'.
    - Even-indexed rows start with '-' but do not end with '-'.
    - Odd-indexed rows do not start with '-' but end with '-'.
    
    Args:
        grid (list of lists): A 2D list representing the grid.

    Returns:
        str: A formatted string representation of the grid.
    """
    formatted_rows = []
    for i, row in enumerate(grid):
        row_str = "-".join(row)  # Join elements of the row with '-'
        if i % 2 == 0:  # Even-indexed rows (0-based)
            formatted_row = f"-{row_str}"  # Start with '-'
        else:  # Odd-indexed rows
            formatted_row = f"{row_str}-"  # End with '-'
        formatted_rows.append(formatted_row.strip('-'))  # Remove any unintended extra '-'
    return "\n".join(formatted_rows)

def print_hexagonal_grid(grid):
    if isinstance(grid, str):
        grid = [row.strip().split('-') for row in grid.strip().split("\n")]

    # grid is a list of lists
    formatted_grid = "\n".join("-".join(row) for row in grid)
    #every second row starts with a '-'
    # for i in range(len(grid)):
    #     if i % 2 == 1:
    #         grid[i] = ['-'] + grid[i]

    formatted_grid = formatted_grid.replace("---", "-")
    formatted_grid = formatted_grid.replace("--", "-")

    print("\n" + formatted_grid + "\n")

def parse_grid(grid_string):
    """Parse the grid from a string representation."""
    return [list(row.strip()) for row in grid_string.strip().split("\n")]


def find_w_position(grid, verbose=0):
    w_row, w_col = None, None
    if isinstance(grid, str):
        grid = [row.split('-') for row in grid.strip().split("\n")]

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'W':
                w_row, w_col = r, c
                if verbose > 1:
                    print(f"Starting position of W: {w_row}, {w_col}")
                return w_row, w_col
    return None, None

def get_neighbors(r, c, grid):
    #check if grid is a list of lists or a string
    if isinstance(grid, str):
        grid = [row.split('-') for row in grid.strip().split("\n")]
    """Get all valid neighboring cells in the hexagonal grid."""
    directions_even = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
    directions_odd = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
    directions = directions_even if r % 2 == 0 else directions_odd

    for dr, dc in directions:
        nr, nc = r + dr, c + dc

        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != 'X':
            yield nr, nc

from collections import deque

def find_reachable_and_escape_paths(grid, w_row, w_col, verbose=0):
    """
    Perform a BFS to find:
    1. All cells reachable from 'W'.
    2. Escape paths that lead to the edge of the grid.
    """
    queue = deque([(w_row, w_col)])
    visited = set()
    escape_paths = set()

    
    while queue:
        r, c = queue.popleft()

        if (r, c) in visited:
            continue
        visited.add((r, c))

        if is_edge(r, c, grid):
            escape_paths.add((r, c))

        for nr, nc in get_neighbors(r, c, grid):
            if (nr, nc) not in visited:
                queue.append((nr, nc))
    
    if verbose > 3:
        print("Visited cells:", visited)
        print("Escape paths:", escape_paths)
    
    return visited, escape_paths


def is_edge(r, c, grid):
    """Check if a cell is on the edge of the grid."""
    return r == 0 or c == 0 or r == len(grid) - 1 or c == len(grid[0]) - 1

def evaluate_and_place_obstacles(gridstring, num_obstacles, verbose=0):
    
    if isinstance(gridstring, str):
        original_grid = [row.split('-') for row in gridstring.strip().split("\n")]
    else:
        original_grid = deepcopy(gridstring)

    processed_grid = evaluate_and_place_obstacles_original(gridstring, num_obstacles, verbose=verbose)
    
    #test if the new_grid has no escape paths
    w_row, w_col = find_w_position(processed_grid, verbose)
    _, escape_paths = find_reachable_and_escape_paths(processed_grid, w_row, w_col, verbose = 0)
    if escape_paths:
        print("Testing: Escape paths still in resulting grid found.")
        print("processed grid")
        print_hexagonal_grid(processed_grid)
        print("original grid")
        print_hexagonal_grid(original_grid)
        print("num_obstacles", num_obstacles)   
        return None
    # test if the ammount of obstacles is the same as the input num_obstacles by comparing the number of X's
    num_obstacles_original = sum([row.count('X') for row in original_grid]) 
    num_obstacles_processed = sum([row.count('X') for row in processed_grid])
    num_obstacles_found = num_obstacles_processed -num_obstacles_original
    if verbose > 4:
        print("num obstacles found:", num_obstacles_found)
        print("num obstacles original:", num_obstacles_original)
        print("num obstacles processed:", num_obstacles_processed)
        print("num obstacles input:", num_obstacles)
        print("")
    if num_obstacles_found != num_obstacles:
        print("Testing: Ammount of obstacles is wrong.")
        print("processed grid")
        print_hexagonal_grid(processed_grid)
        print("original grid")
        print_hexagonal_grid(original_grid)
        print("num_obstacles", num_obstacles)
        print("Ammount of obstacles is wrong.")
        return None
    
    #check if each row has the same amount of items
    if not check_line_item_counts(processed_grid, original_grid):
        print("Testing: Mismatch in counts per line.")
        print("processed grid")
        print_hexagonal_grid(processed_grid)
        print("original grid")
        print_hexagonal_grid(original_grid)
        print("num_obstacles", num_obstacles)
        return processed_grid

    if verbose > 3:
        print("All clear")
    return processed_grid

def check_line_item_counts(grid1, grid2):
    """Check if each line in the grid has the same number of items."""
    item_x = 'X' # Item to check
    item_o = 'O'	

    for row1, row2 in zip(grid1, grid2):
        if row1.count(item_x) + row1.count(item_o) != row2.count(item_x) + row2.count(item_o):
            print("row1", row1)
            print("row2", row2) 
            return False
    return True

def evaluate_and_place_obstacles_original(gridstring, num_obstacles, verbose=0):
    """
    Evaluate all possible combinations of placing obstacles at the neighbors of 'W'
    and determine if all escape paths can be blocked.
    """

    w_row, w_col = find_w_position(gridstring, verbose)
    if verbose >2:
        print("w_row and w_col", w_col, w_row)
    
    if isinstance(gridstring, str):
        grid = [row.split('-') for row in gridstring.strip().split("\n")]
    else:
        grid = gridstring
    
    original_grid = deepcopy(grid)

    if num_obstacles == 0:
        return original_grid
    if w_row is None or w_col is None:
        raise ValueError("No Wasp ('W') found in the grid.")

    # Get neighbors of 'W'
    neighbors = list(get_neighbors(w_row, w_col, grid))
    if verbose > 1:
        print(f"Direct neighbors of W: {[(r, c) for r, c in neighbors]}")
        print_hexagonal_grid(grid)
        print("type grid", type(grid))

    # Generate all combinations of neighbors for placing obstacles
    neighbor_combinations = list(combinations(neighbors, num_obstacles))
    if verbose > 2:
        print(f"Trying {len(neighbor_combinations)} combinations of neighbors for {num_obstacles}.")
        print_hexagonal_grid(grid)

    # Try each combination
    for combo in neighbor_combinations:
        # Make a copy of the grid
        test_grid = deepcopy(grid)       
        for r,c in combo:
            # Place obstacles in the current combination
            if 0 <= r < len(test_grid) and 0 <= c < len(test_grid[0]):  # Check bounds
                test_grid[r][c] = 'X'
            else:
                print(f"Invalid position: ({r}, {c})")


        # Check if escape paths are blocked
        _, escape_paths = find_reachable_and_escape_paths(test_grid, w_row, w_col)
        if not escape_paths:  # If all paths are blocked
            if verbose > 4:
                print("verbose", verbose)
                print(f"Blocking combination found: {combo}")
            for r,c in combo:
                original_grid[r][c] = 'X'
            return original_grid    
            # return "\n".join("-".join(row) for row in test_grid)  # Return the updated grid
        else:
            for r, c in combo:
                test_grid[r][c] = 'O'

    # check W position if any neighbours are on the edge than block them 
    # before considering other neighbours
    test_grid = deepcopy(original_grid)
    combo_0 = []
    # for r, c in get_neighbors(w_row, w_col, test_grid):
    #     if is_edge(r, c, test_grid):
    #         test_grid[r][c] = 'X'
    #         combo_0.append((r, c))
    #         num_obstacles -= 1

    visited, escape_paths = find_reachable_and_escape_paths(test_grid, w_row, w_col, verbose = verbose)
    if verbose > 3:
        print("extend to visited")
    # sort visited count to get the most visited cells
    # dict cannot sort
    if verbose > 2:
        print("num obstacles", num_obstacles)
        print("After blocking edge neighbors")
        print_hexagonal_grid(test_grid)
        # print("escape paths", escape_paths)
    

    # Try to find combinations to block the escape paths starting with the most frequent ones
    # Attempt to block escape paths using num_obstacle
    num = num_obstacles
    if verbose>2:
        print("num", num)   
    pos_to_visit = [pos for pos in visited]
    if verbose >5:
        print("pos_to_visit", pos_to_visit[0:10])

    neighbours_w = list(get_neighbors(w_row, w_col, test_grid))

    # Combine neighbors of W and positions to visit into one set of combinations
   # Generate all combinations: 3 from neighbours_w and 1 from pos_to_visit
    all_combos = product(combinations(neighbours_w, num_obstacles-1), combinations(pos_to_visit, 1))

    
    # Step 1: Direct neighbors of W
    stage_1_positions = set(neighbours_w)

    # Step 2: Neighbors of neighbors of W
    stage_2_positions = set()
    for pos in stage_1_positions:
        stage_2_positions.update(get_neighbors(pos[0],pos[1], test_grid))  # `neighbours(pos)` should return neighbors of `pos`

    if verbose> 2: print("stage_2_positions", stage_2_positions)
    # Step 3: Neighbors of neighbors of neighbors of W
    stage_3_positions = set()
    for pos in stage_2_positions:
        stage_3_positions.update(get_neighbors(pos[0],pos[1], test_grid))

    stage_4_positions = set() # Neighbors of neighbors of neighbors of neighbors of W
    for pos in stage_3_positions:
        stage_4_positions.update(get_neighbors(pos[0],pos[1], test_grid))

    stage_5_positions = set() # Neighbors of neighbors of neighbors of neighbors of W
    for pos in stage_4_positions:
        if verbose > 4: print("pos4", pos)
        stage_5_positions.update(get_neighbors(pos[0],pos[1], test_grid))
    
    stage_6_positions = set() # Neighbors of neighbors of neighbors of neighbors of W
    for pos in stage_5_positions:
        stage_6_positions.update(get_neighbors(pos[0],pos[1], test_grid))

    if verbose >3: print("len positions", len(stage_1_positions), len(stage_2_positions), len(stage_3_positions), len(stage_4_positions), len(stage_5_positions))  

    # Combine the three stages
    limited_pos_to_visit = stage_1_positions.union(stage_2_positions).union(stage_3_positions)    
    # Generate combinations
    all_combos = combinations(limited_pos_to_visit, num_obstacles)
    # print(list(len(all_combos)))
    
    for merged_combo in all_combos:
        # merged_combo = combo[0] + combo[1]  # Combine tuples
        if verbose > 5:    
            print("combo", merged_combo) 
        # Create a copy of the grid
        test_grid_1 = deepcopy(test_grid)
        for r, c in merged_combo:
            if 0 <= r < len(test_grid) and 0 <= c < len(test_grid[0]):  # Check bounds
                test_grid_1[r][c] = 'X'
            else:
                print(f"Invalid position: ({r}, {c})")

        # Check if escape paths are blocked
        _, new_escape_paths = find_reachable_and_escape_paths(test_grid_1, w_row, w_col)

        if not new_escape_paths:  # If all paths are blocked
            if verbose > 2:
                print(f"Blocking combination found after extended blocking: {combo}")
                print(list(get_neighbors(w_row, w_col, test_grid)))
                print_hexagonal_grid(test_grid_1)
            for r, c in merged_combo:
                original_grid[r][c] = 'X'
            for r, c in combo_0:
                original_grid[r][c] = 'X'
            return original_grid
    print("lvl 4 needed")
    limited_pos_to_visit = stage_1_positions.union(stage_2_positions).union(stage_3_positions).union(stage_4_positions)

    all_combos = combinations(limited_pos_to_visit, num_obstacles)
    # print(list(len(all_combos)))
    
    for merged_combo in all_combos:
        # merged_combo = combo[0] + combo[1]  # Combine tuples
        if verbose > 5:    
            print("combo", merged_combo) 
        # Create a copy of the grid
        test_grid_1 = deepcopy(test_grid)
        for r, c in merged_combo:
            if 0 <= r < len(test_grid) and 0 <= c < len(test_grid[0]):  # Check bounds
                test_grid_1[r][c] = 'X'
            else:
                print(f"Invalid position: ({r}, {c})")
        # Check if escape paths are blocked
        _, new_escape_paths = find_reachable_and_escape_paths(test_grid_1, w_row, w_col)

        if not new_escape_paths:  # If all paths are blocked
            if verbose > 2:
                print(f"Blocking combination found after extended blocking: {combo}")
                print_hexagonal_grid(test_grid_1)
            for r, c in merged_combo:
                original_grid[r][c] = 'X'
            for r, c in combo_0:
                original_grid[r][c] = 'X'
            return original_grid
        

    if verbose >3: print("lvl 5 needed")

    if verbose >3:  print("num_obstacles", num_obstacles)
    print_hexagonal_grid(test_grid)
    limited_pos_to_visit = stage_1_positions.union(stage_2_positions).union(stage_3_positions).union(stage_4_positions).union(stage_5_positions)
    # check if 4,9 is in limited_pos_to_visit
  
    if verbose >4:
        print_test_grid = deepcopy(test_grid)
        print_test_grid_2 = deepcopy(test_grid)


        for r in range(0, len(grid)):
            for c in range(0, len(grid[0])):
                if (r,c) in limited_pos_to_visit:
                    print("r,c", r, c)  
                    print_test_grid[r][c] = f"{r}{c}"
                print_test_grid_2[r][c] = f"{r}{c}"

        print_hexagonal_grid(print_test_grid)  
        print_hexagonal_grid(print_test_grid_2)  

        r = 4
        c = 8

    if verbose >3:
        if (r,c) in limited_pos_to_visit:
            print("r,c", r, c)  
            print("48 is in combo")
            print(len(grid),len(grid[0]),len(grid[1]))
        else:
            print("limited_pos_to_visit", limited_pos_to_visit)
        print_test_grid[r][c] = f"{r}{c}"


    all_combos = combinations(limited_pos_to_visit, num_obstacles)
    # print(list(len(all_combos)))
    
    for merged_combo in all_combos:
        # merged_combo = combo[0] + combo[1]  # Combine tuples
        if verbose > 5:    
            print("combo", merged_combo) 
        # Create a copy of the grid
        test_grid_1 = deepcopy(test_grid)
        for r, c in merged_combo:
                if 0 <= r < len(test_grid) and 0 <= c < len(test_grid[0]):  # Check bounds
                    test_grid_1[r][c] = 'X'
                else:
                    print(f"Invalid position: ({r}, {c})")
        # Check if escape paths are blocked
        _, new_escape_paths = find_reachable_and_escape_paths(test_grid_1, w_row, w_col)

        if not new_escape_paths:  # If all paths are blocked
            if verbose > 2:
                print(f"Blocking combination found after extended blocking lvl5: {combo}")
                print_hexagonal_grid(test_grid_1)
            for r, c in merged_combo:
                original_grid[r][c] = 'X'
            for r, c in combo_0:
                original_grid[r][c] = 'X'
            return original_grid
        
    if verbose >3: print("lvl 6 needed")
    limited_pos_to_visit = stage_1_positions.union(stage_2_positions).union(stage_3_positions).union(stage_4_positions).union(stage_5_positions).union(stage_6_positions)

    all_combos = combinations(limited_pos_to_visit, num_obstacles)
    # print(list(len(all_combos)))
    
    for merged_combo in all_combos:
        # merged_combo = combo[0] + combo[1]  # Combine tuples
        if verbose > 5:    
            print("combo", merged_combo) 
        # Create a copy of the grid
        test_grid_1 = deepcopy(test_grid)
        for r, c in merged_combo:
            if 0 <= r < len(test_grid) and 0 <= c < len(test_grid[0]):  # Check bounds
                test_grid_1[r][c] = 'X'
            else:
                print(f"Invalid position: ({r}, {c})")
        # Check if escape paths are blocked
        _, new_escape_paths = find_reachable_and_escape_paths(test_grid_1, w_row, w_col)

        if not new_escape_paths:  # If all paths are blocked
            if verbose > 2:
                print(f"Blocking combination found after extended blocking lvl5: {combo}")
                print_hexagonal_grid(test_grid_1)
            for r, c in merged_combo:
                original_grid[r][c] = 'X'
            for r, c in combo_0:
                original_grid[r][c] = 'X'
            return original_grid
        
    print("No combination blocks all escape paths.")
    print("original grid")
    return grid


if __name__ == "__main__":
    grid_string = """
    O-X-X-O-X-
    -O-O-O-X-O
    X-O-W-O-O-
    -O-X-X-X-X
    O-X-X-O-O-
    """
    grid_string = """
X-X-O-X-O-X-X-O-X-X-
-X-X-O-O-X-X-X-W-X-X
O-O-O-O-X-X-X-O-O-X-
-X-O-O-X-O-O-O-X-X-X
O-X-X-X-X-O-O-O-X-X-
-X-X-O-O-O-X-X-X-X-O
O-X-O-O-O-X-X-X-O-X-
-O-O-X-O-X-O-X-X-O-X"""

    grid_string = """
X-O-O-O-O-O-O-O-O-X-
-O-X-X-O-O-O-O-O-W-O
O-O-X-O-O-O-O-O-X-O-
-O-O-O-O-O-X-X-O-X-X
X-O-O-O-O-O-O-O-O-O-
-X-O-O-X-X-O-O-O-O-O
O-O-O-X-X-O-O-O-O-X-
-X-O-O-O-X-X-X-X-X-X
"""
    grid_string = """
    X-X-O-X-O-O-O-X-O-O-O-O-O-X-O-O-
-O-O-X-X-X-X-O-O-X-X-O-O-X-O-O-O
X-O-O-O-O-O-X-X-W-O-X-O-O-O-O-O-
-O-O-X-X-X-O-O-O-O-X-X-X-O-X-O-O
    """
    grid_string = """
X-X-O-O-X-O-O-X-X-O-
-O-X-O-X-O-W-O-X-O-O
O-O-O-O-O-O-O-O-O-X-
-O-O-O-O-O-O-X-O-O-O
O-X-X-O-O-X-O-X-O-O-
-O-O-O-O-X-X-X-O-O-X
X-X-O-O-O-O-X-O-X-O-
-X-O-O-O-X-O-O-O-O-O
X-O-O-O-O-O-O-X-X-O-
-O-X-O-O-O-O-O-X-O-O
O-X-X-O-X-O-X-O-O-X-
-O-O-O-O-X-O-O-O-X-O
    """
    grid_string = """
X-X-O-X-X-X-O-O-X-O-O-X-
-X-X-O-O-O-O-X-O-X-O-O-O
O-O-O-X-O-X-X-X-O-X-X-O-
-O-X-X-O-X-O-O-O-X-O-O-O
O-O-O-X-O-O-X-X-O-O-X-O-
-O-X-O-X-O-O-O-X-X-X-X-O
X-O-O-X-O-X-O-O-X-O-O-O-
-X-O-X-O-O-X-O-O-O-O-X-O
X-X-O-O-W-O-X-O-O-O-O-X-
-O-O-O-O-X-O-X-O-O-X-O-O
O-O-O-O-X-O-O-O-O-X-X-O-
-O-O-O-X-X-O-O-O-X-X-X-O
"""
    grid_string = """
X-X-O-X-O-O-X-O-O-O-O-O-
-O-X-X-O-X-X-X-O-O-O-O-O
O-O-O-O-O-O-X-X-X-X-X-X-
-O-O-O-O-O-O-O-O-X-O-O-O
X-X-O-X-O-O-X-O-O-O-O-X-
-O-O-X-O-X-O-O-X-O-O-X-O
X-O-X-X-X-X-O-X-O-X-O-O-
-O-O-O-O-X-O-O-O-O-O-O-O
X-O-X-X-O-O-O-X-O-W-X-O-
-O-O-O-O-X-O-X-X-O-O-X-O
X-O-O-O-X-O-O-O-O-O-X-O-
-O-X-O-X-O-O-O-O-X-X-O-O
"""
    grid_string = """
X-X-O-O-X-O-O-X-X-O-
-O-X-O-X-O-W-O-X-O-O
O-O-O-O-O-O-O-O-O-X-
-O-O-O-O-O-O-X-O-O-O
O-X-X-O-O-X-O-X-O-O-
-O-O-O-O-X-X-X-O-O-X
X-X-O-O-O-O-X-O-X-O-
-X-O-O-O-X-O-O-O-O-O
X-O-O-O-O-O-O-X-X-O-
-O-X-O-O-O-O-O-X-O-O
O-X-X-O-X-O-X-O-O-X-
-O-O-O-O-X-O-O-O-X-O
"""
    grid_string = """
    X-X-O-O-X-X-X-O-
    -O-O-O-X-O-O-O-O
    O-O-X-X-O-X-O-X-
    -X-O-O-O-O-O-W-X
    X-O-O-O-X-O-O-O-
    -O-O-O-O-O-X-O-O
    O-X-X-O-X-X-O-X-
    -O-O-X-O-O-O-O-O
    """
    wrong_grid = """
    X-X-X-O-O-X-X-X-
    -X-X-X-O-X-X-O-X
    O-X-O-X-X-O-O-X-
    -X-X-O-O-O-O-W-X
    O-X-O-X-O-O-O-O-X
    -X-X-X-O-O-O-X-X
    O-X-X-O-O-X-X-X-
    -O-O-X-X-X-O-O-O
    """
#Direct neighbors of W: [(2, 6), (3, 6), (4, 6), (4, 7)]
#Blocking combination found after extended blocking: ((3, 6), (4, 6), (4, 7))
    my_try="""
X-X-X-O-O-X-X-O-
-X-X-X-O-X-X-3-X
O-X-O-X-X-O-O-X-
-X-X-O-O-O-O-W-X
O-X-O-X-O-O-O-1-
-X-X-X-O-O-O-X-X
O-X-X-O-O-X-X-X-
-O-O-X-2-X-O-O-O 
    """
    #2624 -> 2361 out
    grid_string = """ 
X-X-X-O-O-X-X-O-
-X-X-X-O-X-X-O-X
O-X-O-X-X-O-O-X-
-X-X-O-O-O-O-W-X
O-X-O-X-O-O-O-O-
-X-X-X-O-O-O-X-X
O-X-X-O-O-X-X-X-
-O-O-X-O-X-O-O-O 
    """

    grid = parse_grid(grid_string)

    print("Initial Grid:")
    print_hexagonal_grid(grid_string)
    verbose = 0
    num_obstacles = 4  # Set the maximum number of obstacles to place
    num_obstacles= 2
    num_obstacles = 4
    num_obstacles = 3
    num_obstacles = 4
    num_obstacles = 5
    num_obstacles = 3 #2364 -> 2364
    try:
        grid = evaluate_and_place_obstacles(grid_string, num_obstacles=num_obstacles, verbose=verbose)
        print("\nUpdated Grid:")
        print_hexagonal_grid(grid)
    except ValueError as e:
        print(str(e))

# %%
