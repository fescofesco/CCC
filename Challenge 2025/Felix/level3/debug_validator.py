def calculate_position_and_time(paces):
    '''Calculate position and time using level2 logic'''
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


def debug_sequence_generation(target_pos):
    """Debug why position calculation is wrong"""
    direction = 1 if target_pos > 0 else -1
    target = abs(target_pos)
    
    print(f'\n=== Debugging position {target_pos} ===')
    print(f'Target: {target} moves in direction {direction}')
    print()
    
    # Check valley patterns
    print('Valley patterns:')
    for min_pace in range(5, 0, -1):
        valley_moves = 2 * (5 - min_pace) + 1
        print(f'  min_pace={min_pace}: valley gives {valley_moves} moves')
    
    print()
    
    # Build the sequence using current logic
    sequence = [0]
    min_pace = 1
    valley_moves = 9
    extra_moves = target - valley_moves
    
    print(f'Extra moves needed: {extra_moves}')
    print(f'Building: 0 → {5*direction} → ({extra_moves} extra {5*direction}s) → valley → {5*direction} → 0')
    print()
    
    # Current code logic
    sequence.append(5 * direction)
    for _ in range(extra_moves):
        sequence.append(5 * direction)
    for pace in range(4, 0, -1):
        sequence.append(pace * direction)
    for pace in range(1, 6):
        sequence.append(pace * direction)
    sequence.append(0)
    
    print(f'Generated sequence: {sequence}')
    
    # Analyze
    position, time_used = calculate_position_and_time(sequence)
    print(f'\nResult: position={position}, expected={target_pos}')
    print(f'Time used: {time_used}')
    
    # Count the pieces
    print(f'\nBreakdown:')
    print(f'  Initial 5: 1 move')
    print(f'  Extra 5s: {extra_moves} moves')
    print(f'  Down valley (4→3→2→1): 4 moves')
    print(f'  Up valley (1→2→3→4→5): 5 moves')
    print(f'  Total moves: 1 + {extra_moves} + 4 + 5 = {1 + extra_moves + 4 + 5}')
    
    return position == target_pos


# Test problematic cases
if __name__ == "__main__":
    test_cases = [-13, 12, -20, -10]
    
    for pos in test_cases:
        correct = debug_sequence_generation(pos)
        print(f'{"✓" if correct else "✗"} Result is {"correct" if correct else "WRONG"}')
        print('-' * 60)
