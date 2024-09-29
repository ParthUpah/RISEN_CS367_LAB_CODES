import heapq

class PuzzleState:
    def _init_(self, board, parent=None, move="", depth=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def _lt_(self, other):
        return self.cost < other.cost

def heuristic(board, goal):
    return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
               for b, g in ((board.index(i), goal.index(i)) for i in range(1, 9)))

def get_neighbors(state):
    neighbors = []
    board = state.board
    empty_index = board.index(0)
    moves = []
    if empty_index % 3 > 0:  # Can move left
        moves.append((-1, "left"))
    if empty_index % 3 < 2:  # Can move right
        moves.append((1, "right"))
    if empty_index // 3 > 0:  # Can move up
        moves.append((-3, "up"))
    if empty_index // 3 < 2:  # Can move down
        moves.append((3, "down"))
    for move, direction in moves:
        new_board = board[:]
        new_board[empty_index], new_board[empty_index + move] = new_board[empty_index + move], new_board[empty_index]
        neighbors.append(PuzzleState(new_board, state, direction, state.depth + 1))
    return neighbors

def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    closed_set = set()
    while open_set:
        _, current = heapq.heappop(open_set)
        if current.board == goal:
            path = []
            while current.parent:
                path.append(current.move)
                current = current.parent
            return path[::-1]
        closed_set.add(tuple(current.board))
        for neighbor in get_neighbors(current):
            if tuple(neighbor.board) in closed_set:
                continue
            neighbor.cost = neighbor.depth + heuristic(neighbor.board, goal)
            heapq.heappush(open_set, (neighbor.cost, neighbor))
    return None

start_board = [4, 1, 2, 7, 5, 3, 8, 0, 6]
goal_board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
start_state = PuzzleState(start_board)
path = a_star(start_state, goal_board)

if path:
    print("Path to solution:", path)
else:
    print("No solution found.")