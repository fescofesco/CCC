import random

def is_valid_placement(matrix, row, col, orientation):
    """Check if a desk can be placed at the specified position without adjacency."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    if orientation == "horizontal" and col + 1 < len(matrix[0]):
        if matrix[row][col] == '.' and matrix[row][col + 1] == '.':
            # Check adjacency for horizontal desk
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) and matrix[nr][nc] == 'X':
                    return False
            nr, nc = row, col + 2  # Extra check for space to the right
            if nc < len(matrix[0]) and matrix[row][nc] == 'X':
                return False
            return True
    elif orientation == "vertical" and row + 1 < len(matrix):
        if matrix[row][col] == '.' and matrix[row + 1][col] == '.':
            # Check adjacency for vertical desk
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) and matrix[nr][nc] == 'X':
                    return False
            nr, nc = row + 2, col  # Extra check for space below
            if nr < len(matrix) and matrix[nr][col] == 'X':
                return False
            return True
    return False

def brute_force_placement(x, y, desk_count):
    while True:
        matrix = [['.'] * x for _ in range(y)]
        desks_placed = 0
        attempts = 0
        
        while desks_placed < desk_count and attempts < 10000:
            row, col = random.randint(0, y - 1), random.randint(0, x - 1)
            orientation = random.choice(["horizontal", "vertical"])
            
            if is_valid_placement(matrix, row, col, orientation):
                if orientation == "horizontal":
                    matrix[row][col] = 'X'
                    matrix[row][col + 1] = 'X'
                else:
                    matrix[row][col] = 'X'
                    matrix[row + 1][col] = 'X'
                desks_placed += 1
            attempts += 1
        
        if desks_placed == desk_count:
            return '\n'.join(''.join(row) for row in matrix)

# Test the function with a 4x10 grid and 9 desks
result = brute_force_placement(4, 10, 9)
print(result)
