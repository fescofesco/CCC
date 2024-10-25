# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:57:12 2024

@author: felix

RockPaperScissors_lvl3.py

"""


import os
from pathlib import Path





def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory, excluding those with 'example' in their name."""
    input_files = []
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files


def parse_file(file_path):
    """Parse the contents of a single input file."""
    with open(file_path, "r") as file:
        lines = file.readlines()
        number_of_tournaments = int(lines[0].split()[0])  # First line: number of tournaments
        number_of_fighters = int(lines[0].split()[1])  # First line: number of fighters
        all_fighters = [line.strip() for line in lines[1:number_of_tournaments + 1]]  # Rest are fights
        
    return number_of_tournaments, number_of_fighters, all_fighters


def find_fighting_styles(counts):
    """Create a string representing the fighting styles based on the counts provided."""
    styles_R = int(counts.split("R")[0])
    styles_P = int(counts.split("R")[1].split("P")[0].strip())
    styles_S = int(counts.split("P")[1].split("S")[0].strip())
   
    styles = [styles_R, styles_P, styles_S]
   
    return styles

def arrange_styles_for_tournament(styles):
    """Arrange styles to allow a valid tournament ensuring R's are eliminated."""
    # Start with all fighters
    arrangement = []
    
    # Split fighters into groups
    count_R = styles[0]
    count_P = styles[1]
    count_S = styles[2]
    
    print("R P S")
    print(count_R,count_P,count_S)
    

  
    
    # Ensure there's at least one S in the final string
    if count_S == 0:
        print("Error: There must be at least one 'S' for the tournament.")
        return None

    # Build the arrangement ensuring R's are eliminated
    
    while count_R > 0 or count_P > 0 or count_S > 0:
        # Try to place fighters in a way that allows for R elimination
     
        if count_R > 2  and count_P >0:
            arrangement.append('R')
            arrangement.append('R')
            arrangement.append('R')
            arrangement.append('P')
            count_R = count_R - 3
            count_P -= 1

        elif count_R ==2 and count_P==1:
            arrangement.append('R')
            arrangement.append('S')
            arrangement.append('R')
            arrangement.append('P')
            
            
            count_R = count_R - 2
            count_P -= 1
            count_S -= 1
            

        elif  count_R == 1 and count_P ==1:
            arrangement.append('R')
            arrangement.append('P')
            count_R -= 1
            count_P -= 1
            
        elif count_P > 0:
            arrangement.append('P')
            count_P -= 1
            
        elif count_S > 0:
            arrangement.append('S')
            count_S -= 1
        
        else:
            print("error")
            break
             
        
        print(count_R,count_P,count_S)
    
    arrangment = ''.join(arrangement)
    
    if [styles[0], styles[1], styles[2]] != [arrangment.count("R"),arrangment.count("P"),arrangment.count("S")]:
        print("attenttion, not fitting")
        print(" R P S")
        print(styles[0], styles[1], styles[2])
        print(arrangment.count("R"),arrangment.count("P"),arrangment.count("S"))
       
    def is_power_of_two(n):
        return (n > 0) and (n & (n - 1)) == 0

    arr_length = len(arrangement)
    
    if is_power_of_two(arr_length):
        print(f"The length {arr_length} is a power of 2.")
    else:
        print(f"The length {arr_length} is not a power of 2.")

    return arrangment




def save_output(output_data, input_file_name):
    """Save the results to an output file with the .out extension."""
    
    # Extract the base file name (remove directory structure)
    base_file_name = Path(input_file_name).name
    
    # Replace .in with .out and modify the example name
    output_file_name = base_file_name.replace(".in", ".out").replace("example", "example_mysolution")
    
    # Define the output directory
    output_dir = Path("./Output/level3")
    
    # Ensure the directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the full output file path
    output_file_path = output_dir / output_file_name
    
    # Print debug information
    print(f"Saving output to: {output_file_path}")
    
    try:
        # Write the output data to the file
        with open(output_file_path, "w") as file:
            for result in output_data:
                file.write(result + "\n")
        print("File saved successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")


def save_output_lvl2(output_data, input_file_name,number_of_tournaments, number_of_fighters):
    """Save the results to an output file with the .out extension."""
    
    # Extract the base file name (remove directory structure)
    base_file_name = Path(input_file_name).name
    
    # Replace .in with .out and modify the example name
    output_file_name = base_file_name.replace("level3", "level3_dummy").replace("example", "example_mysolution")
    
    # Define the output directory
    output_dir = Path("./Output/level3_dummy")
    
    # Ensure the directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the full output file path
    output_file_path = output_dir / output_file_name
    
    # Print debug information
    print(f"Saving output to: {output_file_path}")
    
    try:
        # Write the output data to the file
        with open(output_file_path, "w") as file:
            file.write(f"{number_of_tournaments} {number_of_fighters}\n")
            for result in output_data:
                file.write(result + "\n")
        print("File saved successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")

def rock_paper_scissors_lvl3(location):
    
    #Main function to process all input files and generate the output files.
    input_files = load_inputs(location)
    
    for input_file in input_files:
        print(input_file)
        results = []
        
        # Parse the input file
        number_of_tournaments, number_of_fighters, all_fighters = parse_file(input_file)
        
        for fighters in all_fighters:
            
            styles = find_fighting_styles(fighters)
            arrangment = arrange_styles_for_tournament(styles)
            
            # Determine the outcome of the fights
            results.append(arrangment)
        
        # Save the results to the output file
        save_output(results, input_file)
        save_output_lvl2(results, input_file,number_of_tournaments, number_of_fighters)
        
        

# Example of how to call the main function
if __name__ == "__main__":
    location = Path("Input Files/level3")
    rock_paper_scissors_lvl3(location)