import sys

def solve_level3_debug(input_text):
    """Debug version to see what's happening"""
    data = input_text.strip().split()
    if not data:
        return ""

    it = iter(data)
    try:
        n = int(next(it))
    except StopIteration:
        return ""

    outputs = []

    for _ in range(n):
        try:
            pos = int(next(it))
            time_limit = int(next(it))
        except StopIteration:
            break

        print(f"Processing pos={pos}, time_limit={time_limit}", file=sys.stderr)

        if pos == 0:
            seq = ["0"]
            print(f"Case: pos == 0", file=sys.stderr)
        else:
            direction = 1 if pos > 0 else -1
            abs_pos = abs(pos)
            
            print(f"direction={direction}, abs_pos={abs_pos}", file=sys.stderr)
            
            seq = ["0"]
            
            if abs_pos == 1:
                print(f"Case: abs_pos == 1", file=sys.stderr)
                seq.extend([str(5 * direction), "0"])
            elif abs_pos == 2:
                print(f"Case: abs_pos == 2", file=sys.stderr)
                seq.extend([str(5 * direction), str(5 * direction), "0"])
            elif abs_pos <= 5:
                print(f"Case: abs_pos <= 5 (abs_pos={abs_pos})", file=sys.stderr)
                
                moves = []
                if abs_pos == 3:
                    print(f"  Sub-case: abs_pos == 3", file=sys.stderr)
                    moves = [5, 4, 3]
                elif abs_pos == 4:
                    print(f"  Sub-case: abs_pos == 4", file=sys.stderr)
                    moves = [5, 4, 3, 4]
                elif abs_pos == 5:
                    print(f"  Sub-case: abs_pos == 5", file=sys.stderr)
                    moves = [5, 4, 3, 4, 5]
                
                print(f"  moves={moves}", file=sys.stderr)
                seq.extend([str(move * direction) for move in moves])
                seq.append("0")
            else:
                print(f"Case: abs_pos > 5", file=sys.stderr)
                moves = []
                # Go down from 5
                for cost in range(5, 1, -1):  # 5, 4, 3, 2
                    if len(moves) < abs_pos:
                        moves.append(cost)
                
                # Go back up
                for cost in range(3, 6):  # 3, 4, 5
                    if len(moves) < abs_pos:
                        moves.append(cost)
                
                # If still need more, repeat pattern
                while len(moves) < abs_pos:
                    moves.append(5)
                
                seq.extend([str(move * direction) for move in moves[:abs_pos]])
                seq.append("0")

        print(f"Final seq: {seq}", file=sys.stderr)
        outputs.append(" ".join(seq))

    return "\n".join(outputs) + "\n"

# Test
test_input = "1\n5 39"
result = solve_level3_debug(test_input)
print("Result:", result)