# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:57:12 2024

@author: felix

RockPaperScissors_lvl2.py

"""

#import pandas as pd
#import numpy as np
import os
from pathlib import Path

# Outcome mapping for Rock-Paper-Scissors
outcome_map = {
    "PR": "P", "PS": "S", "PP": "P",
    "RP": "P", "RR": "R", "RS": "R",
    "SS": "S", "SR": "R", "SP": "S"
}







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
        fights = [line.strip() for line in lines[1:number_of_tournaments + 1]]  # Rest are fights
        
    return number_of_tournaments, number_of_fighters, fights



def determine_outcome(fights,fighters):
    """Determine the outcome after 2 rounds using the outcome map."""
    ### first round
    results = []
    for i in range(0,int(fighters),2):
         fight = f"{fights[i]}{fights[i+1]}"  # Create a fight string like "PR"
         result = outcome_map.get(fight, "Invalid")  # Use the map to determine the result
         results.append(result)  # Append the result
         
    results= ''.join(results)
    return results



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
    
    # Write the output data to the file
    with open(output_file_path, "w") as file:
        for result in output_data:
            file.write(result + "\n")

def rock_paper_scissors_lvl2(location):
    """Main function to process all input files and generate the output files."""
    input_files = load_inputs(location)
    
    for input_file in input_files:
        results = []

        # Parse the input file
        number_of_tournaments, number_of_fighters, all_fights = parse_file(input_file)
        
        for fight in all_fights:
            results_first_round = determine_outcome(fight,number_of_fighters)
            number_of_fighters_second_round = number_of_fighters / 2
            result_second_round = determine_outcome(results_first_round,number_of_fighters_second_round)
            
            # Determine the outcome of the fights
            results.append(result_second_round)
        
        # Save the results to the output file
        save_output(results, input_file)

# Example of how to call the main function
if __name__ == "__main__":
    location = Path("Input Files/level2")
    location = Path("Output/level3_dummy")
    
    # def rename_files(location):
    
    
    #     # Iterate over all files in the directory
    #     for file in location.glob("*.out"):
    #         # Get the file name without directory and extension
    #         new_name = file.name.replace(".out", ".in")
            
    #         # Add 'lvl2_' prefix to the new name
    #         new_name = "lvl2_" + new_name
            
    #         # Construct the new file path
    #         new_file_path = file.with_name(new_name)
            
    #         # Rename the file
    #         file.rename(new_file_path)
    #         print(f"Renamed '{file}' to '{new_file_path}'")
    
    # # Call the function to rename the files
   


    # location = Path("./Output/level3")
    # rename_files(location)
    # output_dir = Path("./Output/level3")
    rock_paper_scissors_lvl2(location)
