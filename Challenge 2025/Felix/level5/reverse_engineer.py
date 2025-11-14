"""Reverse engineer: What sequences create the expected path?"""

expected_path = [
    (0,0), (-1,0), (-2,0), (-3,0), (-3,1), (-4,1), (-5,2), (-5,3),
    (-6,3), (-6,4), (-6,5), (-6,6), (-6,6), (-7,6), (-7,7), (-7,8),
    (-7,9), (-6,9)
]

print("Movements needed to create expected path:")
print("="*70)

x_movements = []
y_movements = []

for i in range(1, len(expected_path)):
    prev_x, prev_y = expected_path[i-1]
    curr_x, curr_y = expected_path[i]
    dx = curr_x - prev_x
    dy = curr_y - prev_y
    
    x_movements.append(dx)
    y_movements.append(dy)
    
    print(f"Move {i-1}: ({prev_x:3d},{prev_y:3d}) → ({curr_x:3d},{curr_y:3d}), delta=({dx:2d},{dy:2d})")

print("\n" + "="*70)
print("X movements:", x_movements)
print("Y movements:", y_movements)

print("\n" + "="*70)
print("Given sequences from file:")
x_seq = [0, -5, -4, -3, -2, -3, -4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
y_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 2, 3, 4, 5, 0, 0]

print("X sequence:", x_seq)
print("Y sequence:", y_seq)

print("\n" + "="*70)
print("KEY INSIGHT:")
print("Expected X movements:", x_movements)
print("Expected Y movements:", y_movements)
print("\nX movements are:", [-1, -1, -1, 0, -1, -1, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 1])
print("Y movements are:", [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0])

print("\nX pace -5 means moving at velocity -5, which moves 1 unit left per time step")
print("Y pace 5 means moving at velocity 5, which moves 1 unit up per time step")
print("Pace 0 means not moving (velocity 0)")

print("\nSo if X_pace is non-zero, X moves ±1")
print("And if Y_pace is non-zero, Y moves ±1")
print("Both can happen simultaneously!")
