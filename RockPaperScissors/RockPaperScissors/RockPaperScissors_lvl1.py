# -*- coding: utf-8 -*-
"""
Spyder Editor

RockPaperScissors_lvl1.py

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

location = Path("Input Files/level1")

def load_inputs(location, ending=".in"):
    """Load all input files with the specified ending from the directory."""
    input_files = []
    for file_name in os.listdir(location):
        if file_name.endswith(ending):
            input_files.append(os.path.join(location, file_name))
    return input_files

def parse_file(file_path):
    """Parse the contents of a single input file."""
    with open(file_path, "r") as file:
        lines = file.readlines()
        number_of_rounds = int(lines[0].strip())  # First line: number of rounds
        fights = [line.strip() for line in lines[1:number_of_rounds + 1]]  # Rest are fights
    return number_of_rounds, fights

def determine_outcome(fights):
    """Determine the outcome of each fight using the outcome map."""
    results = []
    for fight in fights:
        results.append(outcome_map.get(fight, "Invalid"))  # Use the map to find the result
    return results

def save_output(output_data, input_file_name):
    """Save the results to an output file with the .out extension."""
    output_file_name = input_file_name.replace(".in", ".out")
    with open(output_file_name, "w") as file:
        for result in output_data:
            file.write(result + "\n")

def rock_paper_scissors(location):
    """Main function to process all input files and generate the output files."""
    input_files = load_inputs(location)
    for input_file in input_files:
        # Parse the input file
        number_of_rounds, fights = parse_file(input_file)
        
        # Determine the outcome of the fights
        results = determine_outcome(fights)
        
        # Save the results to the output file
        save_output(results, input_file)

# Example of how to call the main function
if __name__ == "__main__":
    rock_paper_scissors(location)
