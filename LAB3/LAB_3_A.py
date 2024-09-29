import heapq
import time

# Constants
DIRECTIONS = [(2, 0), (-2, 0), (0, 2), (0, -2)]  # Possible jump directions
BOARD_SIZE = 7

class MarbleSolitaire:
    def _init_(self):
        # Initial board configuration
        self.board = [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        self.start_state = self._serialize_board()

    def _serialize_board(self):
        return tuple(tuple(row) for row in self.board)

    def _is_valid_move(self, x1, y1, x2, y2):
        # Check if the move is valid: jumping over a marble into an empty space
        if 0 <= x2 < BOARD_SIZE and 0 <= y2 < BOARD_SIZE:
            if self.board[x1][y1] == 1 and self.board[x2][y2] == 0:
                xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
                return self.board[xm][ym] == 1
        return False

    def _make_move(self, x1, y1, x2, y2):
        # Make the move and return a new board state
        new_board = [row[:] for row in self.board]
        new_board[x1][y1] = 0
        new_board[x2][y2] = 1
        xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
        new_board[xm][ym] = 0
        return tuple(tuple(row) for row in new_board)

    def get_possible_moves(self):
        moves = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == 1:  # If there's a marble
                    for dx, dy in DIRECTIONS:
                        x2, y2 = x + dx, y + dy
                        if self._is_valid_move(x, y, x2, y2):
                            moves.append((x, y, x2, y2))
        return moves

    def heuristic1(self):
        # Number of remaining marbles
        return sum(row.count(1) for row in self.board)

    def heuristic2(self):
        # Distance to goal position
        return sum(abs(x - 3) + abs(y - 3) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if self.board[x][y] == 1)

    def goal_test(self):
        # Goal is to have only one marble in the center
        return sum(row.count(1) for row in self.board) == 1 and self.board[3][3] == 1

    def a_star_search(self):
        start_time = time.time()
        frontier = []
        heapq.heappush(frontier, (self.heuristic1(), self.start_state))
        explored = set()
        parent_map = {self.start_state: None}

        while frontier:
            _, current_state = heapq.heappop(frontier)
            if current_state in explored:
                continue
            explored.add(current_state)
            self.board = [list(row) for row in current_state]
            if self.goal_test():
                return self._reconstruct_path(parent_map, current_state), time.time() - start_time
            for x1, y1, x2, y2 in self.get_possible_moves():
                next_state = self._make_move(x1, y1, x2, y2)
                if next_state not in explored:
                    heapq.heappush(frontier, (self.heuristic1(), next_state))
                    parent_map[next_state] = current_state
        return None

    def best_first_search(self):
        start_time = time.time()
        frontier = []
        heapq.heappush(frontier, (self.heuristic1(), self.start_state))
        explored = set()
        parent_map = {self.start_state: None}

        while frontier:
            _, current_state = heapq.heappop(frontier)
            if current_state in explored:
                continue
            explored.add(current_state)
            self.board = [list(row) for row in current_state]
            if self.goal_test():
                return self._reconstruct_path(parent_map, current_state), time.time() - start_time
            for x1, y1, x2, y2 in self.get_possible_moves():
                next_state = self._make_move(x1, y1, x2, y2)
                if next_state not in explored:
                    heapq.heappush(frontier, (self.heuristic1(), next_state))
                    parent_map[next_state] = current_state
        return None

    def priority_queue_search(self):
        start_time = time.time()
        frontier = []
        heapq.heappush(frontier, (self.heuristic1(), self.start_state))
        explored = set()
        parent_map = {self.start_state: None}

        while frontier:
            _, current_state = heapq.heappop(frontier)
            if current_state in explored:
                continue
            explored.add(current_state)
            self.board = [list(row) for row in current_state]
            if self.goal_test():
                return self._reconstruct_path(parent_map, current_state), time.time() - start_time
            for x1, y1, x2, y2 in self.get_possible_moves():
                next_state = self._make_move(x1, y1, x2, y2)
                if next_state not in explored:
                    heapq.heappush(frontier, (self.heuristic1(), next_state))
                    parent_map[next_state] = current_state
        return None

    def _reconstruct_path(self, parent_map, state):
        path = []
        while state is not None:
            path.append(state)
            state = parent_map[state]
        path.reverse()  # Reverse the path to get it from start to goal
        return path

    def print_solution_steps(self, path):
        print("Solution Steps:")
        for board_state in path:
            for row in board_state:
                print(' '.join(str(x) for x in row))
            print()  # Print an empty line between steps

    def compare_search_algorithms(self):
        # Priority Queue Search
        pq_path, pq_time = self.priority_queue_search()
        if pq_path:
            print(f"Priority Queue Search Time: {pq_time:.6f} seconds")
            self.print_solution_steps(pq_path)
        else:
            print("Priority Queue Search did not find a solution.")

        # Reset board for next search
        self.board = [list(row) for row in self.start_state] 

        # A* Search
        a_star_path, a_star_time = self.a_star_search()
        if a_star_path:
            print(f"A* Search Time: {a_star_time:.6f} seconds")
            self.print_solution_steps(a_star_path)
        else:
            print("A* Search did not find a solution.")

        # Reset board for next search
        self.board = [list(row) for row in self.start_state] 

        # Best First Search
        best_first_path, best_first_time = self.best_first_search()
        if best_first_path:
            print(f"Best-First Search Time: {best_first_time:.6f} seconds")
            self.print_solution_steps(best_first_path)
        else:
            print("Best-First Search did not find a solution.")


if _name_ == "_main_":
    solitaire = MarbleSolitaire()
    solitaire.compare_search_algorithms()