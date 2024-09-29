def is_goal(state):
    return state == "WWW_EEE"

def get_neighbors(state):
    neighbors = []
    empty_index = state.index("_")

    # Try moving east-bound rabbits ("E") to the right
    if empty_index > 0 and state[empty_index - 1] == 'E':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index - 1] = new_state[empty_index - 1], new_state[empty_index]
        neighbors.append(''.join(new_state))
    
    # Try jumping east-bound rabbits ("E") to the right
    if empty_index > 1 and state[empty_index - 2] == 'E':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index - 2] = new_state[empty_index - 2], new_state[empty_index]
        neighbors.append(''.join(new_state))

    # Try moving west-bound rabbits ("W") to the left
    if empty_index < len(state) - 1 and state[empty_index + 1] == 'W':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index + 1] = new_state[empty_index + 1], new_state[empty_index]
        neighbors.append(''.join(new_state))

    # Try jumping west-bound rabbits ("W") to the left
    if empty_index < len(state) - 2 and state[empty_index + 2] == 'W':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index + 2] = new_state[empty_index + 2], new_state[empty_index]
        neighbors.append(''.join(new_state))
    
    return neighbors

def dfs(state, visited):
    if is_goal(state):
        return [state]

    visited.add(state)

    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            path = dfs(neighbor, visited)
            if path:
                return [state] + path

    return None

def solve_rabbit_leap():
    initial_state = "EEE_WWW"
    visited = set()
    solution = dfs(initial_state, visited)
    
    if solution:
        return solution
    else:
        return "No solution found"

# Run the solution
solution = solve_rabbit_leap()
for step in solution:
    print(step)