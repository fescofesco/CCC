"""Compare the expected solution with our generated solution."""

# Expected (correct) solution
expected_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0]
expected_y = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

# Our generated solution
generated_x = [0, 0, 0, 0, 0, 5, 4, 3, 3, 4, 5, 0, 0, 0, 0, 0]
generated_y = [0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, -5, -4, -5, 0]

ax, ay = 3, 0

print("COMPARISON:")
print("="*80)
print(f"Expected X length: {len(expected_x)}")
print(f"Expected Y length: {len(expected_y)}")
print(f"Generated X length: {len(generated_x)}")
print(f"Generated Y length: {len(generated_y)}")

print("\n" + "="*80)
print("KEY INSIGHT - Looking at the TIMING:")
print("="*80)

print("\nExpected X sequence:")
print("  Starts with 15 zeros (indices 0-14)")
print("  Then moves: [5, 4, 3, 3, 4, 5, 0] (indices 15-21)")

print("\nOur X sequence:")
print("  Starts with 5 zeros (indices 0-4)")
print("  Then moves: [5, 4, 3, 3, 4, 5, 0] (indices 5-11)")
print("  Then 5 more zeros (indices 12-15)")

print("\nExpected Y sequence:")
print("  Moves up: [0, 5, 4, 5, 0] (indices 0-4)")
print("  Then 23 zeros (indices 5-27)")
print("  Then moves down: [-5, -4, -5, 0] (indices 28-31)")

print("\nOur Y sequence:")
print("  Moves up: [0, 5, 4, 5, 0] (indices 0-4)")
print("  Then 7 zeros (indices 5-11)")
print("  Then moves down: [-5, -4, -5, 0] (indices 12-15)")

print("\n" + "="*80)
print("CRITICAL DIFFERENCE:")
print("="*80)
print("The expected solution has MORE WAIT PERIODS (zeros) between movements!")
print("- Y finishes moving up at index 4")
print("- X waits until index 15 to start moving (10 extra zeros)")
print("- X finishes at index 21")
print("- Y waits until index 28 to move down (6 extra zeros)")
print()
print("Our solution has LESS waiting - movements happen immediately after each other.")
print()
print("Both follow the SAME PATH, just different TIMING.")
print()
print("The sequences DON'T need to be the same length!")
print("Expected: X=22, Y=32 (10 difference)")
print("Generated: X=16, Y=16 (0 difference)")

print("\n" + "="*80)
print("TESTING: Do both reach the same positions?")
print("="*80)

# Simulate both
def simulate(x_seq, y_seq):
    x_pos, y_pos = 0, 0
    path = [(x_pos, y_pos)]
    
    max_len = max(len(x_seq), len(y_seq))
    for i in range(max_len):
        x_pace = x_seq[i] if i < len(x_seq) else 0
        y_pace = y_seq[i] if i < len(y_seq) else 0
        
        if x_pace > 0:
            x_pos += 1
        elif x_pace < 0:
            x_pos -= 1
        if y_pace > 0:
            y_pos += 1
        elif y_pace < 0:
            y_pos -= 1
        
        path.append((x_pos, y_pos))
    
    return path

expected_path = simulate(expected_x, expected_y)
generated_path = simulate(generated_x, generated_y)

print(f"\nExpected unique positions: {set(expected_path)}")
print(f"Generated unique positions: {set(generated_path)}")
print(f"\nSame positions? {set(expected_path) == set(generated_path)}")

print(f"\nExpected final position: {expected_path[-1]}")
print(f"Generated final position: {generated_path[-1]}")
