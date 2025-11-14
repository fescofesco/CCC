"""Debug: trace through our build_sequences_from_path to see what it produces."""

# The path our BFS finds
path = [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (6,2), (6,1), (6,0)]

print("Path segments:")
print("="*80)

# Manually trace what segments are created
segments = []
i = 0
while i < len(path) - 1:
    x1, y1 = path[i]
    x2, y2 = path[i + 1]
    dx = x2 - x1
    dy = y2 - y1
    
    if dx != 0:
        axis = 'x'
        direction = 1 if dx > 0 else -1
    elif dy != 0:
        axis = 'y'
        direction = 1 if dy > 0 else -1
    else:
        i += 1
        continue
    
    # Count consecutive
    count = 1
    j = i + 1
    while j < len(path) - 1:
        nx1, ny1 = path[j]
        nx2, ny2 = path[j + 1]
        ndx = nx2 - nx1
        ndy = ny2 - ny1
        
        if axis == 'x' and ndx * direction > 0 and ndy == 0:
            count += 1
            j += 1
        elif axis == 'y' and ndy * direction > 0 and ndx == 0:
            count += 1
            j += 1
        else:
            break
    
    segments.append({'axis': axis, 'direction': direction, 'count': count})
    print(f"Segment {len(segments)}: {axis} {'+' if direction > 0 else '-'} {count} steps")
    i = j

print(f"\nTotal segments: {len(segments)}")

print("\n" + "="*80)
print("Building sequences:")
print("="*80)

def generate_efficient_move_sequence(count, direction):
    if count == 0:
        return []
    elif count == 1:
        return [5 * direction]
    elif count == 2:
        return [5 * direction, 5 * direction]  
    elif count <= 8:
        patterns = {
            3: [5, 4, 5],
            4: [5, 4, 4, 5],
            5: [5, 4, 3, 4, 5],
            6: [5, 4, 3, 3, 4, 5],
            7: [5, 4, 3, 2, 3, 4, 5],
            8: [5, 4, 3, 2, 2, 3, 4, 5]
        }
        return [p * direction for p in patterns[count]]
    else:
        extra_at_1 = count - 9
        seq = []
        for pace in range(5, 0, -1):
            seq.append(pace * direction)
        for _ in range(extra_at_1):
            seq.append(1 * direction)
        for pace in range(2, 6):
            seq.append(pace * direction)
        return seq

x_seq = [0]
y_seq = [0]

for seg_num, segment in enumerate(segments, 1):
    move_seq = generate_efficient_move_sequence(segment['count'], segment['direction'])
    pace_count = len(move_seq) + 1
    
    print(f"\nSegment {seg_num} ({segment['axis']} {segment['count']}):")
    print(f"  Move sequence: {move_seq}")
    print(f"  Pace count (with ending 0): {pace_count}")
    
    if segment['axis'] == 'x':
        print(f"  Adding to X: {move_seq} + [0]")
        print(f"  Adding to Y: {pace_count} zeros")
        x_seq.extend(move_seq)
        x_seq.append(0)
        y_seq.extend([0] * pace_count)
    else:
        print(f"  Adding to Y: {move_seq} + [0]")
        print(f"  Adding to X: {pace_count} zeros")
        y_seq.extend(move_seq)
        y_seq.append(0)
        x_seq.extend([0] * pace_count)
    
    print(f"  X length now: {len(x_seq)}, Y length now: {len(y_seq)}")

print("\n" + "="*80)
print("Final sequences:")
print("="*80)
print(f"X ({len(x_seq)}): {x_seq}")
print(f"Y ({len(y_seq)}): {y_seq}")

print("\n" + "="*80)
print("PROBLEM IDENTIFIED:")
print("="*80)
print("Our code creates 3 segments that execute one after another.")
print("Expected solution has the same 3 segments BUT with extra wait periods.")
print("\nThe issue: We don't add extra zeros BETWEEN segments for coordination!")
