import random

def generate_k_sat(k, m, n):
    """
    Generate a uniform random k-SAT problem.
    
    Parameters:
    k (int): The length of each clause.
    m (int): The number of clauses.
    n (int): The number of variables.
    
    Returns:
    list: A list of clauses, where each clause is a list of literals.
    """
    if k > n:
        raise ValueError("k cannot be greater than n (number of variables).")
    
    clauses = []
    
    for _ in range(m):
        # Randomly select k distinct variable indices
        variable_indices = random.sample(range(1, n + 1), k)
        # Randomly decide to negate each selected variable or not
        clause = [random.choice([-var, var]) for var in variable_indices]
        clauses.append(clause)
    
    return clauses

def print_k_sat(clauses):
    """Print the k-SAT problem in a readable format."""
    for clause in clauses:
        print(f"({' OR '.join(f'~x{abs(lit)}' if lit < 0 else f'x{lit}' for lit in clause)})")

if _name_ == "_main_":
    # Input parameters
    k = int(input("Enter the length of each clause (k): "))
    m = int(input("Enter the number of clauses (m): "))
    n = int(input("Enter the number of variables (n): "))

    # Generate k-SAT problem
    k_sat_problem = generate_k_sat(k, m, n)

    # Print the generated k-SAT problem
    print("\nGenerated k-SAT Problem:")
    print_k_sat(k_sat_problem)