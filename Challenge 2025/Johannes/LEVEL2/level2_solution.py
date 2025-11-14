import sys
import os

def solve_level2(input_text):
    """
    Solve Level 2 problem: track position and time with movement costs
    
    :param input_text: The input as a string
    :return: The output as a string
    """
    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip() != ""]
    
    if not lines:
        return ""

    # First line: number of sequences
    N = int(lines[0])
    
    results = []
    
    # Process each sequence line
    for i in range(1, N + 1):
        parts = lines[i].split()
        paces = [int(x) for x in parts]

        position = 0
        total_time = 0

        for p in paces:
            if p > 0:
                # Move forward by 1
                position += 1
                total_time += p  # time cost equals pace magnitude
            elif p < 0:
                # Move backward by 1
                position -= 1
                total_time += -p  # abs(p)
            else:
                # Stand still: no space change, but 1 time unit
                total_time += 1

        results.append(f"{position} {total_time}")
    
    return '\n'.join(results) + '\n'


def main():
    """Main function for stdin/stdout processing"""
    # Read all non-empty lines
    lines = [line.strip() for line in sys.stdin if line.strip() != ""]
    if not lines:
        return

    # First line: number of sequences
    N = int(lines[0])

    # Process each sequence line
    for i in range(1, N + 1):
        parts = lines[i].split()
        paces = [int(x) for x in parts]

        position = 0
        total_time = 0

        for p in paces:
            if p > 0:
                # Move forward by 1
                position += 1
                total_time += p  # time cost equals pace magnitude
            elif p < 0:
                # Move backward by 1
                position -= 1
                total_time += -p  # abs(p)
            else:
                # Stand still: no space change, but 1 time unit
                total_time += 1

        print(f"{position} {total_time}")


def test_with_files():
    """Test function that processes .in files and generates .out files"""
    level2_dir = r"c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL2\level2"
    
    # Find all .in files
    in_files = [f for f in os.listdir(level2_dir) if f.endswith('.in')]
    
    for in_file in in_files:
        print(f"Processing {in_file}...")
        
        # Read input file
        in_path = os.path.join(level2_dir, in_file)
        with open(in_path, 'r') as f:
            input_text = f.read()
        
        # Solve the problem
        output_text = solve_level2(input_text)
        
        # Write output file
        out_file = in_file.replace('.in', '_generated.out')
        out_path = os.path.join(level2_dir, out_file)
        with open(out_path, 'w') as f:
            f.write(output_text)
        
        print(f"Generated {out_file}")
        
        # If there's an expected output file, compare
        expected_out_file = in_file.replace('.in', '.out')
        expected_out_path = os.path.join(level2_dir, expected_out_file)
        
        if os.path.exists(expected_out_path):
            with open(expected_out_path, 'r') as f:
                expected_output = f.read()
            
            if output_text == expected_output:
                print(f"✅ {in_file}: Generated output matches expected output!")
            else:
                print(f"❌ {in_file}: Generated output differs from expected output")
                print(f"Expected:\n{repr(expected_output)}")
                print(f"Generated:\n{repr(output_text)}")
        else:
            print(f"ℹ️  {in_file}: No expected output file found")
        
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_with_files()
    else:
        main()