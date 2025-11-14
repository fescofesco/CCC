from pathlib import Path

# Test file
test_file = Path(r"C:\Users\felix\CCC\CCC\Challenge 2025\Input\level1\level1_0_example.in")

with open(test_file, 'r') as f:
    lines = f.readlines()

# Parse first line
first_line = lines[0].strip()
parts = first_line.split('→')
num_sequences = int(parts[0].strip())

print(f"Number of sequences: {num_sequences}")

total_sum = 0

# Process the next num_sequences lines
for i in range(1, num_sequences + 1):
    if i < len(lines):
        line = lines[i].strip()
        print(f"Line {i}: '{line}'")
        if '→' in line:
            arrow_parts = line.split('→')
            numbers_str = arrow_parts[1].strip()
            print(f"  Numbers string: '{numbers_str}'")

            if numbers_str:
                numbers = [int(n) for n in numbers_str.split()]
                line_sum = sum(numbers)
                total_sum += line_sum
                print(f"  Numbers: {numbers}, Sum: {line_sum}")
            else:
                print(f"  No numbers on this line")

print(f"\nTotal sum: {total_sum}")

# Save to file
output_file = Path(r"C:\Users\felix\CCC\CCC\Challenge 2025\Felix\Outputs\level1\level1_0_example.out")
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, 'w') as f:
    f.write(str(total_sum))

print(f"Output saved to {output_file}")
