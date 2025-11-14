import sys
sys.path.append('..')
from level4 import calculate_position_and_time, validate_sequence


def validate_level4_output(input_file, output_file, show_details=False):
    """Validate a level 4 output file."""
    print(f"\n{'='*70}")
    print(f"Validating: {output_file.split('\\')[-1] if '\\' in output_file else output_file}")
    print(f"{'='*70}")
    
    # Read input
    with open(input_file) as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    
    cases = []
    for i in range(1, n + 1):
        line = lines[i].strip()
        pos_part, time_limit_str = line.split()
        x_pos, y_pos = map(int, pos_part.split(','))
        time_limit = int(time_limit_str)
        cases.append((x_pos, y_pos, time_limit))
    
    # Read output
    with open(output_file) as f:
        output_lines = [line.strip() for line in f.readlines()]
    
    errors = []
    valid_count = 0
    
    for case_num, (x_pos, y_pos, time_limit) in enumerate(cases, 1):
        # Each case has: X-sequence line, Y-sequence line, blank line
        idx = (case_num - 1) * 3
        
        if idx >= len(output_lines):
            errors.append(f"Case {case_num}: Missing output")
            continue
        
        x_seq_str = output_lines[idx]
        y_seq_str = output_lines[idx + 1] if idx + 1 < len(output_lines) else ""
        
        try:
            x_sequence = list(map(int, x_seq_str.split()))
            y_sequence = list(map(int, y_seq_str.split()))
        except:
            errors.append(f"Case {case_num}: Cannot parse sequences")
            continue
        
        # Validate X sequence
        x_valid, x_msg = validate_sequence(x_sequence, x_pos, time_limit)
        if not x_valid:
            errors.append(f"Case {case_num} X ({x_pos},{y_pos}): {x_msg}")
            continue
        
        # Validate Y sequence
        y_valid, y_msg = validate_sequence(y_sequence, y_pos, time_limit)
        if not y_valid:
            errors.append(f"Case {case_num} Y ({x_pos},{y_pos}): {y_msg}")
            continue
        
        valid_count += 1
        
        if show_details:
            x_pos_calc, x_time = calculate_position_and_time(x_sequence)
            y_pos_calc, y_time = calculate_position_and_time(y_sequence)
            print(f"  ✓ Case {case_num:3d}: ({x_pos:3d},{y_pos:3d}) "
                  f"X-time={x_time:3d}/{time_limit}, Y-time={y_time:3d}/{time_limit}")
    
    # Show errors
    if errors:
        print(f"\nErrors found ({len(errors)}):")
        for err in errors[:20]:
            print(f"  ✗ {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors)-20} more errors")
    else:
        print(f"\n  ✓ All {valid_count} cases are VALID!")
    
    # Summary
    print(f"\n{'─'*70}")
    print(f"Summary: {valid_count}/{len(cases)} valid, {len(errors)}/{len(cases)} errors")
    print(f"{'─'*70}")
    
    return len(errors) == 0


if __name__ == "__main__":
    import os
    
    base_input = r"C:\Users\felix\CCC\CCC\Challenge 2025\Input\level4"
    base_output = r"C:\Users\felix\CCC\CCC\Challenge 2025\Felix\Outputs\level4"
    
    test_files = [
        ("level4_0_example", True),   # (name, show_details)
        ("level4_1_small", False),
        ("level4_2_large", False),
    ]
    
    all_valid = True
    for filename, show_details in test_files:
        input_file = os.path.join(base_input, f"{filename}.in")
        output_file = os.path.join(base_output, f"{filename}.out")
        
        if os.path.exists(input_file) and os.path.exists(output_file):
            valid = validate_level4_output(input_file, output_file, show_details)
            all_valid = all_valid and valid
        else:
            print(f"\n✗ Files not found for {filename}")
            all_valid = False
    
    print(f"\n{'='*70}")
    print(f"FINAL RESULT: {'✓ ALL VALID' if all_valid else '✗ ERRORS FOUND'}")
    print(f"{'='*70}")
