def calculate_position_and_time(paces):
    """Calculate position and time using level2 logic"""
    position = 0
    total_time = 0
    for p in paces:
        if p > 0:
            position += 1
            total_time += p
        elif p < 0:
            position -= 1
            total_time += abs(p)
        else:
            total_time += 1
    return position, total_time


def validate_all_rules(seq_str, expected_pos, time_limit, seq_num=0):
    """Validate a sequence against all rules"""
    try:
        paces = list(map(int, seq_str.strip().split()))
    except:
        return False, f"Cannot parse sequence"
    
    errors = []
    
    # Rule 1: Start and end with 0
    if paces[0] != 0:
        errors.append(f"Does not start with 0 (starts with {paces[0]})")
    if paces[-1] != 0:
        errors.append(f"Does not end with 0 (ends with {paces[-1]})")
    
    # Rule 2: From 0, can only go to ±5
    for i in range(len(paces)-1):
        if paces[i] == 0 and paces[i+1] != 0:
            if abs(paces[i+1]) != 5:
                errors.append(f"From 0 at idx {i} to {paces[i+1]} (must be ±5)")
    
    # Rule 3: To 0, can only come from ±5
    for i in range(len(paces)-1):
        if paces[i] != 0 and paces[i+1] == 0:
            if abs(paces[i]) != 5:
                errors.append(f"To 0 at idx {i+1} from {paces[i]} (must be ±5)")
    
    # Rule 4: Between non-zero paces, can only change by ±1
    for i in range(len(paces)-1):
        if paces[i] != 0 and paces[i+1] != 0:
            diff = abs(paces[i+1] - paces[i])
            if diff > 1:
                errors.append(f"At idx {i}: {paces[i]} to {paces[i+1]} (change={diff}, must be ≤1)")
    
    # Calculate position and time
    position, time_used = calculate_position_and_time(paces)
    
    if position != expected_pos:
        errors.append(f"Position mismatch: got {position}, expected {expected_pos}")
    if time_used > time_limit:
        errors.append(f"Time exceeded: {time_used} > {time_limit}")
    
    if errors:
        return False, "; ".join(errors)
    
    return True, f"Valid (pos={position}, time={time_used}/{time_limit})"


def validate_file(input_file, output_file, max_check=None, show_all=False):
    """Validate an entire output file"""
    print(f"\n{'='*70}")
    print(f"Validating: {output_file.split('\\')[-1]}")
    print(f"{'='*70}")
    
    # Read input
    with open(input_file) as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    targets = [list(map(int, lines[i].strip().split())) for i in range(1, n+1)]
    
    # Read output
    with open(output_file) as f:
        outputs = f.readlines()
    
    if max_check:
        targets = targets[:max_check]
        outputs = outputs[:max_check]
    
    total = len(targets)
    valid_count = 0
    error_count = 0
    errors_detail = []
    
    for i, (seq, (pos, tl)) in enumerate(zip(outputs, targets)):
        valid, msg = validate_all_rules(seq, pos, tl, i+1)
        if valid:
            valid_count += 1
            if show_all:
                print(f"  ✓ Seq {i+1:4d}: {msg}")
        else:
            error_count += 1
            errors_detail.append(f"  ✗ Seq {i+1:4d}: {msg}")
    
    # Show errors
    if errors_detail:
        print(f"\nErrors found ({error_count}):")
        for err in errors_detail[:20]:  # Show first 20 errors
            print(err)
        if len(errors_detail) > 20:
            print(f"  ... and {len(errors_detail)-20} more errors")
    else:
        print(f"\n  ✓ All {valid_count} sequences are VALID!")
    
    # Summary
    print(f"\n{'─'*70}")
    print(f"Summary: {valid_count}/{total} valid, {error_count}/{total} errors")
    print(f"{'─'*70}")
    
    return error_count == 0


if __name__ == "__main__":
    import os
    
    base_input = r"C:\Users\felix\CCC\CCC\Challenge 2025\Input\level3"
    base_output = r"C:\Users\felix\CCC\CCC\Challenge 2025\Felix\Outputs\level3"
    
    test_files = [
        ("level3_0_example", None, True),   # (name, max_check, show_all)
        ("level3_1_small", 100, False),
        ("level3_2_large", 100, False),
    ]
    
    all_valid = True
    for filename, max_check, show_all in test_files:
        input_file = os.path.join(base_input, f"{filename}.in")
        output_file = os.path.join(base_output, f"{filename}.out")
        
        if os.path.exists(input_file) and os.path.exists(output_file):
            valid = validate_file(input_file, output_file, max_check, show_all)
            all_valid = all_valid and valid
        else:
            print(f"\n✗ Files not found for {filename}")
            all_valid = False
    
    print(f"\n{'='*70}")
    print(f"FINAL RESULT: {'✓ ALL VALID' if all_valid else '✗ ERRORS FOUND'}")
    print(f"{'='*70}")
