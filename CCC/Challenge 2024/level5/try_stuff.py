from typing import List, Tuple, Dict, Set


def get_possible_desk_positions(grid: List[List[str]]) -> List[Tuple[str, int, int]]:
    positions = []
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            # Horizontal desk
            if j + 1 < cols and grid[i][j] == '.' and grid[i][j + 1] == '.':
                positions.append(('H', i, j))
            # Vertical desk
            if i + 1 < rows and grid[i][j] == '.' and grid[i + 1][j] == '.':
                positions.append(('V', i, j))
    return positions


def desks_conflict(pos1, pos2) -> bool:
    # Determine if two desks conflict
    cells1 = desk_cells(pos1)
    cells2 = desk_cells(pos2)
    # Check for overlap
    if set(cells1) & set(cells2):
        return True
    # Check for adjacency
    for cell1 in cells1:
        for cell2 in cells2:
            if abs(cell1[0] - cell2[0]) <= 1 and abs(cell1[1] - cell2[1]) <= 1:
                if cell1 != cell2:
                    return True
    return False


def desk_cells(pos) -> List[Tuple[int, int]]:
    orientation, i, j = pos
    if orientation == 'H':
        return [(i, j), (i, j + 1)]
    else:
        return [(i, j), (i + 1, j)]


def build_conflict_graph(positions) -> Dict:
    conflict_graph = {pos: set() for pos in positions}
    for idx, pos1 in enumerate(positions):
        for pos2 in positions[idx + 1:]:
            if desks_conflict(pos1, pos2):
                conflict_graph[pos1].add(pos2)
                conflict_graph[pos2].add(pos1)
    return conflict_graph


def csp_backtrack(assignment: Dict, positions: List, conflict_graph: Dict, desks_to_place: int) -> Dict:
    if sum(assignment.values()) == desks_to_place:
        return assignment
    if not positions:
        return None
    # Heuristic: Select the variable with the fewest conflicts
    positions.sort(key=lambda pos: len(conflict_graph[pos]))
    pos = positions.pop(0)
    for value in [True, False]:
        if value:
            # Check conflicts
            if any(assignment.get(neigh, False) for neigh in conflict_graph[pos]):
                continue
        assignment[pos] = value
        result = csp_backtrack(assignment.copy(), positions.copy(), conflict_graph, desks_to_place)
        if result is not None:
            return result
        assignment.pop(pos)
    return None


def place_desks(grid: List[List[str]], desks_to_place: int) -> List[List[str]]:
    positions = get_possible_desk_positions(grid)
    conflict_graph = build_conflict_graph(positions)
    assignment = {}
    result = csp_backtrack(assignment, positions, conflict_graph, desks_to_place)
    if result is None:
        print("No valid arrangement found.")
        return grid
    # Place desks according to the assignment
    for pos, placed in result.items():
        if placed:
            for i, j in desk_cells(pos):
                grid[i][j] = 'X'
    return grid


if __name__ == '__main__':
    # Example usage
    grid = [['.'] * 12 for _ in range(17)]
    desks_to_place = 39
    placed_grid = place_desks(grid, desks_to_place)
    for row in placed_grid:
        print(''.join(row))
