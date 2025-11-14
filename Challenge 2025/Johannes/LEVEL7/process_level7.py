import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the solution
from level7_solution import solve_level7

def process_all_inputs():
    """Process all Level 7 input files."""
    level7_dir = r"c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL7\level7"
    
    in_files = sorted([f for f in os.listdir(level7_dir) if f.endswith('.in')])
    
    for in_file in in_files:
        print(f"Processing {in_file}...")
        
        in_path = os.path.join(level7_dir, in_file)
        with open(in_path, 'r') as f:
            input_text = f.read()
        
        output_text = solve_level7(input_text)
        
        out_file = in_file.replace('.in', '_generated.out')
        out_path = os.path.join(level7_dir, out_file)
        with open(out_path, 'w') as f:
            f.write(output_text)
        
        print(f"Generated {out_file}")
        print()

if __name__ == "__main__":
    process_all_inputs()
