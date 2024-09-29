from collections import deque

# Check if a state is valid
def is_valid_state(missionaries, cannibals):
    return (missionaries == 0 or missionaries >= cannibals) and (missionaries <= 3 and cannibals <= 3)

# DFS to solve the problem
def dfs_missionaries_cannibals():
    # Initial state: (Missionaries on left, Cannibals on left, Boat on left)
    initial_state = (3, 3, 1)
    goal_state = (0, 0, 0)
    
    # Stack for DFS: (missionaries_left, cannibals_left, boat_position, path)
    stack = [(initial_state, [])]
    
    # Set to track visited states
    visited = set()
    visited.add(initial_state)

    # All possible moves (Missionaries, Cannibals)
    moves = [(1, 0), (2, 0), (1, 1), (0, 1), (0, 2)]

    while stack:
        # 0: Select Current State
        (missionaries_left, cannibals_left, boat_position), path = stack.pop()
        
        # 0: Check for Goal State
        if (missionaries_left, cannibals_left, boat_position) == goal_state:
            return path + [(0, 0, 0)]
        
        # 0: Generate Successors
        for move_missionaries, move_cannibals in moves:
            if boat_position == 1:  # Boat is on the left side
                new_state = (missionaries_left - move_missionaries,
                             cannibals_left - move_cannibals,
                             0)
            else:  # Boat is on the right side
                new_state = (missionaries_left + move_missionaries,
                             cannibals_left + move_cannibals,
                             1)
            
            new_missionaries_left, new_cannibals_left, new_boat_position = new_state
            new_missionaries_right = 3 - new_missionaries_left
            new_cannibals_right = 3 - new_cannibals_left
            
            # 0: Process Successors
            if is_valid_state(new_missionaries_left, new_cannibals_left) and is_valid_state(new_missionaries_right, new_cannibals_right):
                if new_state not in visited:
                    # 0: Push Successor to stack and mark as visited
                    visited.add(new_state)
                    stack.append((new_state, path + [(missionaries_left, cannibals_left, boat_position)]))

    # 0: If no solution is found, terminate
    return None

# Driver code
solution = dfs_missionaries_cannibals()

if solution:
    print("Solution found:")
    for state in solution:
        print(state)  # Print state tuple (missionaries_left, cannibals_left, boat_position)
else:
    print("No solution found.")