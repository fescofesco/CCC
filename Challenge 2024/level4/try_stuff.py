from typing import List

def place_desks(x: int, y: int) -> List[List[str]]:
    """Place desks in an x by y grid with 1x3 desk blocks in every second row or column."""
    matrix = [['.'] * x for _ in range(y)]  # Initialize grid with empty spaces ('.')

    # Determine primary and secondary dimensions
    is_x_primary = x >= y  # True if x is primary, False if y is primary

    # Use every second row or column to place 1x3 desk blocks
    if is_x_primary:
        # Place desks in every second row
        for row in range(0, y, 2):
            for col in range(0, x - 2, 4):  # Step by 4 to leave a gap of 1x3
                matrix[row][col] = 'X'
                matrix[row][col + 1] = 'X'
                matrix[row][col + 2] = 'X'
    else:
        # Place desks in every second column
        for col in range(0, x, 2):
            for row in range(0, y - 2, 4):  # Step by 4 to leave a gap of 1x3
                matrix[row][col] = 'X'
                matrix[row + 1][col] = 'X'
                matrix[row + 2][col] = 'X'

    return matrix


# Example usage
x, y = 10, 9  # Example grid dimensions
grid = place_desks(x, y)

# Display the grid
for row in grid:
    print(' '.join(row))
