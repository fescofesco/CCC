"""Verify that our paths don't violate the safety zone."""
import sys
sys.path.insert(0, r'c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5')

from level5_solution import solve_level5

# Read the example input
with open(r'c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5\level5\level5_0_example.in', 'r') as f:
    input_text = f.read()

# Generate our solution
output_text = solve_level5(input_text)
print("Generated output:")
print(output_text)
print("\n" + "="*60)

# Parse and simulate each test case
lines = output_text.strip().split('\n')
test_cases = [
    {'target': (6, 0), 'asteroid': (3, 0)},
    {'target': (10, 4), 'asteroid': (7, 4)},
    {'target': (-7, -7), 'asteroid': (-4, -4)}
]

idx = 0
for case_num, test_case in enumerate(test_cases):
    print(f"\nTEST CASE {case_num + 1}:")
    print(f"Target: {test_case['target']}, Asteroid: {test_case['asteroid']}")
    
    x_seq_str = lines[idx]
    idx += 1
    y_seq_str = lines[idx]
    idx += 1
    if idx < len(lines) and lines[idx].strip() == '':
        idx += 1
    
    x_seq = list(map(int, x_seq_str.split()))
    y_seq = list(map(int, y_seq_str.split()))
    
    # Simulate the movement
    x_pos, y_pos = 0, 0
    ax, ay = test_case['asteroid']
    
    violation_found = False
    max_steps = max(len(x_seq), len(y_seq))
    
    print(f"\nSimulating {max_steps} steps:")
    for i in range(max_steps):
        # Get pace (or 0 if sequence ended)
        x_pace = x_seq[i] if i < len(x_seq) else 0
        y_pace = y_seq[i] if i < len(y_seq) else 0
        
        # Update position
        if x_pace > 0:
            x_pos += 1
        elif x_pace < 0:
            x_pos -= 1
            
        if y_pace > 0:
            y_pos += 1
        elif y_pace < 0:
            y_pos -= 1
        
        # Check collision (Chebyshev distance)
        dist = max(abs(x_pos - ax), abs(y_pos - ay))
        
        if dist <= 2:
            print(f"❌ Step {i}: Position ({x_pos}, {y_pos}) - Distance to asteroid: {dist} - VIOLATION!")
            violation_found = True
        elif i < 10 or i >= max_steps - 5 or (i % 5 == 0):
            print(f"   Step {i}: Position ({x_pos}, {y_pos}) - Distance to asteroid: {dist}")
    
    print(f"\nFinal position: ({x_pos}, {y_pos})")
    print(f"Target position: {test_case['target']}")
    print(f"Reached target: {(x_pos, y_pos) == test_case['target']}")
    
    if violation_found:
        print("❌ COLLISION DETECTED - Safety zone violated!")
    else:
        print("✅ No collisions - Path is safe!")
    print("="*60)
