from collections import deque

# Check if the state is the goal state
def is_goal_state(state):
    return state == ('W', 'W', 'W', '_', 'E', 'E', 'E')

# Generate possible successor states
def generate_successors(state):
    successors = []
    empty_pos = state.index('_')  # Find the index of the empty stone

    # Define possible moves (one step or two steps)
    possible_moves = [-1, 1, -2, 2]

    for move in possible_moves:
        new_empty_pos = empty_pos + move

        # Ensure the move is within the bounds of the list
        if 0 <= new_empty_pos < len(state):
            # Create a new state by swapping the empty stone with the rabbit
            new_state = list(state)
            new_state[empty_pos], new_state[new_empty_pos] = new_state[new_empty_pos], new_state[empty_pos]
            successors.append(tuple(new_state))

    return successors

# BFS to solve the Rabbit Leap problem
def bfs_rabbit_leap():
    # Initial state (E, E, E, _, W, W, W)
    initial_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
    
    # Queue for BFS: (current_state, path)
    queue = deque([(initial_state, [])])
    
    # Set to track visited states
    visited = set()
    visited.add(initial_state)

    while queue:
        # Select Current State
        current_state, path = queue.popleft()

        # Check for Goal State
        if is_goal_state(current_state):
            return path + [current_state]

        # Generate Possible Moves
        successors = generate_successors(current_state)

        # Process Successors
        for successor in successors:
            if successor not in visited:
                # Add Successor
                visited.add(successor)
                queue.append((successor, path + [current_state]))

    # If no solution is found, terminate
    return None

# Convert state to EEE_WWW format
def format_state(state):
    return ''.join(state)

# Driver code
solution = bfs_rabbit_leap()

if solution:
    print("Solution found:")
    for step in solution:
        print(format_state(step))
else:
    print("No solution found.")