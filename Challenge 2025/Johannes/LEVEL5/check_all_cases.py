"""Check all three test cases."""
import sys
sys.path.insert(0, r'c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5')

from level5_solution import solve_level5

# Read input
with open(r'c:\Users\accou\Code\Coding_Contest\CCC\Challenge 2025\Johannes\LEVEL5\level5\level5_0_example.in', 'r') as f:
    input_text = f.read()

# Generate solution
output = solve_level5(input_text)
lines = [line for line in output.split('\n') if line.strip()]

test_cases = [
    {'name': 'Case 1', 'target': (6, 0), 'asteroid': (3, 0)},
    {'name': 'Case 2', 'target': (10, 4), 'asteroid': (7, 4)},
    {'name': 'Case 3', 'target': (-7, -7), 'asteroid': (-4, -4)}
]

idx = 0
for test in test_cases:
    print(f"\n{'='*60}")
    print(f"{test['name']}: Target {test['target']}, Asteroid {test['asteroid']}")
    print('='*60)
    
    x_seq = list(map(int, lines[idx].split()))
    y_seq = list(map(int, lines[idx + 1].split()))
    idx += 2
    
    # Simulate
    x_pos, y_pos = 0, 0
    ax, ay = test['asteroid']
    
    violations = []
    max_steps = max(len(x_seq), len(y_seq))
    
    for i in range(max_steps):
        x_pace = x_seq[i] if i < len(x_seq) else 0
        y_pace = y_seq[i] if i < len(y_seq) else 0
        
        # Apply movement
        if x_pace > 0:
            x_pos += 1
        elif x_pace < 0:
            x_pos -= 1
        if y_pace > 0:
            y_pos += 1
        elif y_pace < 0:
            y_pos -= 1
        
        # Check distance
        dist = max(abs(x_pos - ax), abs(y_pos - ay))
        if dist <= 2:
            violations.append(f"  Step {i}: pos({x_pos},{y_pos}) dist={dist}")
    
    print(f"Final position: ({x_pos}, {y_pos})")
    print(f"Target matched: {(x_pos, y_pos) == test['target']}")
    
    if violations:
        print(f"\n❌ COLLISIONS FOUND ({len(violations)} violations):")
        for v in violations[:10]:  # Show first 10
            print(v)
        if len(violations) > 10:
            print(f"  ... and {len(violations) - 10} more")
    else:
        print("✅ NO COLLISIONS - Path is safe!")
