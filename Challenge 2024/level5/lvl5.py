from dataclasses import dataclass
from typing import List
import os
from pathlib import Path

@dataclass
class RoomDeskInfo:
    x: int  # Room length (x-axis)
    y: int  # Room height (y-axis)
    desks_to_place: int  # Fixed number of desks to place


def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory."""
    input_files = []
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files


def parse_input(input_string):
    """Parse the input format where each line gives room dimensions and number of desks."""
    lines = input_string.strip().split('\n')
    N = int(lines[0])  # Number of rooms

    room_infos = []
    for i in range(1, N + 1):
        x, y, desk_count = map(int, lines[i].split())
        room_infos.append(RoomDeskInfo(x, y, desk_count))
    return room_infos


def provide_room_matrix(room_infos: List[RoomDeskInfo]) -> List[str]:
    """Generate the room matrix with the specified number of desks without touching each other."""
    results = []

    for room_info in room_infos:
        x, y, desk_count = room_info.x, room_info.y, room_info.desks_to_place

        best_desks_placed = 0
        best_matrix_output = ''
        placed_all_desks = False  # Flag to track if all desks were placed

        for start_horizontally in [True, False]:
            for stop_vert in [True, False]:
                
                # Reset desks_placed and matrix for each attempt
                desks_placed, result_mat = try_table_placement(desk_count, start_horizontally, x, y, stop_vert)
        
                if desks_placed >= desk_count:
                    # We have placed all desks
                    matrix_output = result_mat
                    results.append(matrix_output)
                    placed_all_desks = True  # Set flag to exit both loops
                    break  # Exit inner loop
                
                else:
                    # Keep track of the best attempt
                    if desks_placed > best_desks_placed:
                        best_desks_placed = desks_placed
                        best_matrix_output = result_mat
                        
            if placed_all_desks:  # Check flag to exit outer loop
                break
        else:
            # If we did not place all desks in any attempt, use the best attempt
            results.append(best_matrix_output)
            print(f"Warning: Could not place all desks in room {x}x{y}. Placed {best_desks_placed} desks out of {desk_count}.")

    return results



    desks_placed = 0
    matrix = [['.'] * x for _ in range(y)]
    row_step, col_step = (2, 3) if start_horizontally else (3, 2)
    row_stop, col_stop = (y - 4, x - 5) if start_horizontally else (y - 6, x - 4)

    if start_horizontally:
        for row in range(0, row_stop, row_step):
            for col in range(0, col_stop, col_step):
                if desks_placed >= desk_count:
                    break
                if col + 1 < x:
                    matrix[row][col] = 'X'
                    matrix[row][col + 1] = 'X'
                    desks_placed += 1
            if desks_placed >= desk_count:
                break

    else:
        for row in range(0, row_stop, row_step):
            for col in range(0, col_stop, col_step):
                if desks_placed >= desk_count:
                    break
                if row + 1 < y:
                    matrix[row][col] = 'X'
                    matrix[row + 1][col] = 'X'
                    desks_placed += 1
            if desks_placed >= desk_count:
                break

    # Optional: Attempt to place remaining desks in alternate orientation
    if desks_placed < desk_count:
        for row in range(y):
            for col in range(x):
                if desks_placed >= desk_count:
                    break
                if matrix[row][col] == '.':
                    if start_horizontally and col + 1 < x and matrix[row][col + 1] == '.':
                        if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row, col + 1)]):
                            matrix[row][col] = 'X'
                            matrix[row][col + 1] = 'X'
                            desks_placed += 1
                    elif not start_horizontally and row + 1 < y and matrix[row + 1][col] == '.':
                        if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row + 1, col)]):
                            matrix[row][col] = 'X'
                            matrix[row + 1][col] = 'X'
                            desks_placed += 1

    return desks_placed, '\n'.join(''.join(row) for row in matrix)

def try_table_placementX(desk_count, start_horizontally, x, y, stop_vert):
    desks_placed = 0
    # matrix = [['.'] * (x+1) for _ in range(y+1)]
    matrix = [['.'] * (x) for _ in range(y)]
    # Step 1: Initial Placement in Preferred Orientation
    if start_horizontally: #True
        if stop_vert:
            # Place desks horizontally
            for row in range(0, y, 2):  # Every other row to prevent adjacency
                for col in range(0, x, 3):  # Place desks with spacing
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                    if col + 1 < x:
                        matrix[row][col] = 'X'
                        matrix[row][col + 1] = 'X'
                        desks_placed += 1
                if desks_placed >= desk_count:
                    break
                if row == y-4: #row y-4 important
                    break
                if col == x-6: #row y-4 important
                    break
              
        else:
            
            for col in range(0, x, 3):  # Place desks with spacing
                for row in range(0, y, 2):  # Every other row to prevent adjacency
             
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                    if col + 1 < x:
                        matrix[row][col] = 'X'
                        matrix[row][col + 1] = 'X'
                        desks_placed += 1
                if desks_placed >= desk_count:
                    break
                if row == y-4: #row y-4 important
                    break
                if col == x-6: #row y-4 important
                    break
           
   
    else: #start_horizontally: #False
        # Place desks vertically: True
        if stop_vert:
            for col in range(0, x, 2):  # Every other column to prevent adjacency
                for row in range(0, y, 3):  # Place desks with spacing
         
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                    if row + 1 < y:
                        matrix[row][col] = 'X'
                        matrix[row + 1][col] = 'X'
                        desks_placed += 1
                if desks_placed >= desk_count:
                    break
                if col == x-4: #col x-4 important
                    break
                if row == y-6:
                    break
        else: #start_horizontally: #False
            # Place desks vertically: False
            for row in range(0, y, 3):  # Place desks with spacing
                  for col in range(0, x, 2):  # Every other column to prevent adjacency
                      if desks_placed >= desk_count:
                          break
                      # Ensure we don't go out of bounds
                      if row + 1 < y:
                          matrix[row][col] = 'X'
                          matrix[row + 1][col] = 'X'
                          desks_placed += 1
                  if desks_placed >= desk_count:
                      break
    
                  if row == y-6: # row == y-6 important
                      break
                  if col == x-4: #col x-4 important
                      break
        
    # Step 2: Additional Placement in Alternative Orientation
    if desks_placed < desk_count:
        # Attempt to place additional desks in the alternative orientation
        if start_horizontally:
            # print(start_horizontally)
            # Try placing vertical desks in remaining spaces
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a vertical desk
                        if row + 1 < y and matrix[row + 1][col] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row + 1, col)]):
                                matrix[row][col] = 'X'
                                matrix[row + 1][col] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
            
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a horizontal desk
                        if col + 1 < x and matrix[row][col + 1] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row, col + 1)]):
                                matrix[row][col] = 'X'
                                matrix[row][col + 1] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break

                
        else:
            # Try placing horizontal desks in remaining spaces
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a horizontal desk
                        if col + 1 < x and matrix[row][col + 1] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row, col + 1)]):
                                matrix[row][col] = 'X'
                                matrix[row][col + 1] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
                
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a vertical desk
                        if row + 1 < y and matrix[row + 1][col] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row + 1, col)]):
                                matrix[row][col] = 'X'
                                matrix[row + 1][col] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break

    
    return desks_placed, '\n'.join(''.join(row) for row in matrix)
    # matrix = matrix[:row-1][:col-1]
    
    return desks_placed, '\n'.join(''.join(row) for row in matrix)

def try_table_placement(desk_count, start_horizontally, x, y, stop_vert):
    desks_placed = 0
    # matrix = [['.'] * (x+1) for _ in range(y+1)]
    matrix = [['.'] * (x) for _ in range(y)]
    # Step 1: Initial Placement in Preferred Orientation
    stop = False
    if start_horizontally: #True
        if stop_vert:
            
            for row in range(0, y, 2):  # Every other column to prevent adjacency
                if stop: 
                    break
                for col in range(0, x, 3):  # Place desks with spacing
                    # print("x ","y ", col, " ", row)
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                  
                    if col == x-3:
                        # stop= True
                        break
                    
                    if row == y-2:
                        break
                    
                    if col + 1 < x:
                        matrix[row][col] = 'X'
                        matrix[row][col+1] = 'X'
                        desks_placed += 1
    

                if desks_placed >= desk_count:
                    stop = True
                    break
  
                        
                  
        else:
            
            for col in range(0, x, 3):  # Place desks with spacing
                for row in range(0, y, 2):  # Every other row to prevent adjacency
             
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                    if col + 1 < x:
                        matrix[row][col] = 'X'
                        matrix[row][col + 1] = 'X'
                        desks_placed += 1
                if desks_placed >= desk_count:
                    break
                if row == y-4: #row y-4 important
                    break
                if col == x-6: #row y-4 important
                    break
           
   
    else: #start_horizontally: #False
        # Place desks vertically: True
        if stop_vert:
            #x from top left to right
            #y from top to bottom
            for col in range(0, x, 2):  # Every other column to prevent adjacency
                if stop: 
                    break
                for row in range(0, y, 3):  # Place desks with spacing
                    # print("x ","y ", col, " ", row)
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                  
                    if row == y-3:
                        # stop= True
                        # print("row4", row, col)
                        break
                    
                    if col == x-2:
                        # print("col4", row, col)
                        break
                    
                    if row + 1 < y:
                        matrix[row][col] = 'X'
                        matrix[row + 1][col] = 'X'
                        desks_placed += 1
    

                if desks_placed >= desk_count:
                    stop = True
                    break
               
                    
         
        else: #start_horizontally: #False
            # Place desks vertically: False
            for row in range(0, y, 3):  # Place desks with spacing
                if stop: 
                    break
                # if row == y-2:
                #     # stop= True
                #     print("row4", row, col)
                #     stop = True
                #     break
                
                for col in range(0, x, 2):  # Every other column to prevent adjacency
                    if desks_placed >= desk_count:
                        break
                    # Ensure we don't go out of bounds
                    if row + 1 < y:
                        matrix[row][col] = 'X'
                        matrix[row + 1][col] = 'X'
                        desks_placed += 1
                if desks_placed >= desk_count:
                    break
  
                
                
                if col == x-2:
                    # print("col4", row, col)
                    stop = True
                    break
        
    # Step 2: Additional Placement in Alternative Orientation
    if desks_placed < desk_count:
        # Attempt to place additional desks in the alternative orientation
        if start_horizontally:
#            
            # Try placing VERTICAL desks in remaining spaces  
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if row+3 >= y and col+3 >= x:
                        # print("hey")
                        break
                    if matrix[row][col] == '.':
                        # Try placing a vertical desk
                        if row + 1 < y and matrix[row + 1][col] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row + 1, col)]):
                                matrix[row][col] = 'X'
                                matrix[row + 1][col] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
                
            # Try placing HORIZONTAL desks in remaining spaces
            for row in range(y):
                for col in range(x):
                    # print(row,y,col,x)
                                         
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a horizontal desk
                        if col + 1 < x and matrix[row][col + 1] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row, col + 1)]):
                                matrix[row][col] = 'X'
                                matrix[row][col + 1] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
                   
        else:
            
           
                
            # Try placing HORIZONTAL desks in remaining spaces
            for row in range(y):
                for col in range(x):
                    # print(row,y,col,x)
                    # if row+5 >= y and col+1 >= x:
                        # print("hey")
                        # break
                    
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a horizontal desk
                        if col + 1 < x and matrix[row][col + 1] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row, col + 1)]):
                                matrix[row][col] = 'X'
                                matrix[row][col + 1] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
            
            # Try placing VERTICAL desks in remaining spaces  
            for row in range(y):
                for col in range(x):
                    if desks_placed >= desk_count:
                        break
                    if matrix[row][col] == '.':
                        # Try placing a vertical desk
                        if row + 1 < y and matrix[row + 1][col] == '.':
                            if not has_adjacent_desk(matrix, row, col, x, y, [(row, col), (row + 1, col)]):
                                matrix[row][col] = 'X'
                                matrix[row + 1][col] = 'X'
                                desks_placed += 1
                if desks_placed >= desk_count:
                    break
                
           

    
    return desks_placed, '\n'.join(''.join(row) for row in matrix)

def has_adjacent_desk(matrix, i, j, x, y, desk_cells):
    """Check if any adjacent cells (including diagonally) have a desk."""
    for ci, cj in desk_cells:
        for ni in range(ci - 1, ci + 2):
            for nj in range(cj - 1, cj + 2):
                if (ni, nj) == (ci, cj):
                    continue
                if 0 <= ni < y and 0 <= nj < x:
                    if matrix[ni][nj] == 'X':
                        return True
    return False

def format_output(room_results: List[str]) -> str:
    """Format the results by joining the room matrices."""
    return '\n\n'.join(room_results)


if __name__ == '__main__':
    
    # best_desks = 0 
    
    # desks = 7
    # x = 6
    # y = 5
    
    # # desks = 7
    # x = 5
    # y = 6
    
       
    # desks = 467
    # # horizontally False
    # # stop_vert False
    # # this works
    # x = 45
    # y = 60
    
    # #this does not work
    # desks = 467
    # x = 60
    # y = 45
    
    # desks = 117
    # x = 21
    # y = 31
    
    # desks = 10
    # x = 6
    # y = 8
    # y = 6
    # x =8
    
    # desks = 9
    # x = 4
    # y = 10
   
    # x = 10
    # y = 4
    
    # desks = 8
    # x= 6
    # y=6
    # # x = 22
    # # y = 76
    
    # desks = 5
    # x = 4
    # y =5
    
    # # Warning: Could not place all desks in room 6x8. Placed 9 desks out of 10.
    # # for start_horizontally in [True]:
    # # for start_horizontally in [False]:
    # for start_horizontally in [True,False]:
    #     # for stop_vert in [True, False]:
    #     for stop_vert in [True]:
    #     # for stop_vert in [False]:
    #         deskfound, matrix= try_table_placement(desks, start_horizontally, x,y, stop_vert)
    #         print("deskfound: ", deskfound)
    #         print("start_horizontally:", start_horizontally)
    #         print("stop_vert;", stop_vert)
    #         print(matrix)
       
    #         print("/n")
    #         if deskfound == desks:
    #             best_desks = deskfound
    #             best_result = matrix
    #             print("start_horizontally: ", start_horizontally)
    #             print("stop_vert: ",stop_vert)
    #             print(matrix)
    #             print("/n")
    
    # # desks = 467
    # # x = 45
    # # y = 60
    


# """

    input_location = Path("../Inputs/level5")
    output_location = Path("../Outputs/level5")

    # Load input files
    input_files = load_inputs(input_location)

    for f_p in input_files:
        with open(f_p, "r") as file:
            input_string = file.read()

        # Parse input
        rooms = parse_input(input_string)

        # Generate the room matrices with desks and empty spaces
        room_results = provide_room_matrix(rooms)

        # Format the output
        formatted_output = format_output(room_results)

        # Write the output to the corresponding file
        out_fp = output_location / (Path(f_p).stem + ".out")
        with open(out_fp, "w") as file:
            file.write(formatted_output)
# """