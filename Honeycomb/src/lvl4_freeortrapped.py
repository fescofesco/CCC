#%%
from collections import deque

def print_hexagonal_grid(grid):
    if isinstance(grid, str):
        grid = [row.strip().split('-') for row in grid.strip().split("\n")]
    formatted_grid = "\n".join("-".join(row) for row in grid)
    print("\n" + formatted_grid + "\n")

def find_w_position(grid, verbose=0):
    w_row, w_col = None, None
    if isinstance(grid, str):
        grid = [row.split('-') for row in grid.strip().split("\n")]

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'W':
                w_row, w_col = r, c
                if verbose > 1:
                    print(f"Starting position of W: {w_row}, {w_col}")
                return w_row, w_col
    return None, None

def lvl4_freeOrTrapped(grid, w_row, w_col, verbose=0):
    if isinstance(grid, str):
        grid = [row.split('-') for row in grid.strip().split("\n")]

    directions_even = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
    directions_odd = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]

    def get_neighbors(r, c):
        directions = directions_even if r % 2 == 0 else directions_odd
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != 'X':
                yield nr, nc

    def is_edge(r, c):
        return r == 0 or c == 0 or r == len(grid) - 1 or c == len(grid[0]) - 1

    queue = deque([(w_row, w_col)])
    visited = set()
    visited.add((w_row, w_col))

    while queue:
        r, c = queue.popleft()
        if verbose > 1:
            print(f"Visiting cell ({r}, {c}).")

        if is_edge(r, c):
            if verbose > 0:
                print(f"Reached edge at ({r}, {c}). Returning 'FREE'.")
            return "FREE"

        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
                if verbose > 1:
                    print(f"Adding cell ({nr}, {nc}) to the queue.")

    if verbose > 0:
        print("No path to the edge found. Returning 'TRAPPED'.")
    return "TRAPPED"

if __name__ == "__main__":
    grid_string = """
    X-X-X-O-O-O-O-O-X-O-
    -O-X-O-O-O-X-X-O-O-X
    O-O-X-O-O-O-O-X-O-X-
    -O-O-O-X-O-O-X-O-X-O
    O-O-X-X-O-O-O-X-O-X-
    -O-O-O-X-O-O-O-X-O-O
    O-O-X-O-O-X-W-O-X-X-
    -O-O-O-X-X-X-X-X-O-O
    """

    w_row, w_col = find_w_position(grid_string, verbose=2)
    print("Position in string:", w_row, w_col)
    result = lvl4_freeOrTrapped(grid_string, w_row, w_col, verbose=2)
    print("Result (string):", result)

#print grid
    print_hexagonal_grid(grid_string)
