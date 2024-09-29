import random
import time
from typing import List, Tuple, Dict

def generate_3_sat(m: int, n: int) -> List[List[int]]:
    """
    Generate a uniform random 3-SAT problem.

    Parameters:
    m (int): The number of clauses.
    n (int): The number of variables.

    Returns:
    List[List[int]]: A list of clauses, where each clause is a list of literals.
    """
    clauses = []
    
    for _ in range(m):
        variable_indices = random.sample(range(1, n + 1), 3)  # 3 distinct variables
        clause = [random.choice([-var, var]) for var in variable_indices]  # Negate or not
        clauses.append(clause)
    
    return clauses

class SATSolver:
    def _init_(self, clauses: List[List[int]], n: int):
        self.clauses = clauses
        self.n = n

    def random_solution(self) -> List[int]:
        """Generate a random solution."""
        return [random.choice([0, 1]) for _ in range(self.n)]

    def evaluate_solution(self, solution: List[int]) -> bool:
        """Evaluate if the given solution satisfies all clauses."""
        for clause in self.clauses:
            if not any((literal > 0 and solution[literal - 1]) or (literal < 0 and not solution[-literal - 1]) for literal in clause):
                return False
        return True

    def hill_climbing(self) -> Tuple[List[int], float]:
        """Hill Climbing algorithm for solving 3-SAT."""
        start_time = time.time()
        current_solution = self.random_solution()
        best_solution = current_solution
        while True:
            neighbors = self.get_neighbors(current_solution)
            next_solution = max(neighbors, key=lambda sol: self.evaluate_fitness(sol))
            if self.evaluate_fitness(next_solution) <= self.evaluate_fitness(best_solution):
                break
            best_solution = next_solution
            current_solution = best_solution
        return best_solution, time.time() - start_time

    def beam_search(self, beam_width: int) -> Tuple[List[int], float]:
        """Beam Search algorithm for solving 3-SAT."""
        start_time = time.time()
        current_solutions = [self.random_solution() for _ in range(beam_width)]
        while True:
            new_solutions = []
            for sol in current_solutions:
                new_solutions.extend(self.get_neighbors(sol))
            current_solutions = sorted(new_solutions, key=lambda sol: self.evaluate_fitness(sol), reverse=True)[:beam_width]
            if any(self.evaluate_solution(sol) for sol in current_solutions):
                break
        return current_solutions[0], time.time() - start_time

    def variable_neighborhood_descent(self) -> Tuple[List[int], float]:
        """Variable Neighborhood Descent algorithm for solving 3-SAT."""
        start_time = time.time()
        current_solution = self.random_solution()
        neighborhoods = [self.get_neighbors, self.get_bit_flip_neighbors, self.get_random_neighbors]
        neighborhood_index = 0
        
        while True:
            neighbors = neighborhoods[neighborhood_index](current_solution)
            next_solution = max(neighbors, key=lambda sol: self.evaluate_fitness(sol))
            if self.evaluate_fitness(next_solution) <= self.evaluate_fitness(current_solution):
                neighborhood_index = (neighborhood_index + 1) % len(neighborhoods)
                if neighborhood_index == 0:  # All neighborhoods exhausted
                    break
            current_solution = next_solution
        
        return current_solution, time.time() - start_time

    def get_neighbors(self, solution: List[int]) -> List[List[int]]:
        """Generate neighbors by flipping one bit."""
        return [solution[:i] + [1 - solution[i]] + solution[i+1:] for i in range(self.n)]

    def get_bit_flip_neighbors(self, solution: List[int]) -> List[List[int]]:
        """Generate neighbors by flipping two bits."""
        neighbors = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                new_solution = solution[:]
                new_solution[i] = 1 - new_solution[i]
                new_solution[j] = 1 - new_solution[j]
                neighbors.append(new_solution)
        return neighbors

    def get_random_neighbors(self, solution: List[int]) -> List[List[int]]:
        """Generate a random number of neighbors."""
        num_neighbors = random.randint(1, 5)
        return [self.random_solution() for _ in range(num_neighbors)]

    def evaluate_fitness(self, solution: List[int]) -> int:
        """Calculate fitness based on satisfied clauses."""
        return sum(1 for clause in self.clauses if any((literal > 0 and solution[literal - 1]) or (literal < 0 and not solution[-literal - 1]) for literal in clause))

def compare_algorithms(m: int, n: int) -> Dict[str, Tuple[float, bool]]:
    """Generate a random 3-SAT problem and compare the performance of algorithms."""
    clauses = generate_3_sat(m, n)
    solver = SATSolver(clauses, n)

    results = {}
    for algorithm in ['Hill Climbing', 'Beam Search (width=3)', 'Beam Search (width=4)', 'Variable Neighborhood Descent']:
        if algorithm == 'Hill Climbing':
            solution, exec_time = solver.hill_climbing()
        elif algorithm == 'Beam Search (width=3)':
            solution, exec_time = solver.beam_search(3)
        elif algorithm == 'Beam Search (width=4)':
            solution, exec_time = solver.beam_search(4)
        else:  # Variable Neighborhood Descent
            solution, exec_time = solver.variable_neighborhood_descent()
        
        is_solution = solver.evaluate_solution(solution)
        results[algorithm] = (exec_time, is_solution)
    
    return results

if _name_ == "_main_":
    m_values = [5, 10, 15]  # Different numbers of clauses
    n_values = [5, 7, 10]   # Different numbers of variables

    for m in m_values:
        for n in n_values:
            print(f"\nComparing algorithms for m={m}, n={n}:")
            results = compare_algorithms(m, n)
            for algorithm, (exec_time, is_solution) in results.items():
                print(f"{algorithm}: Execution Time = {exec_time:.4f}s, Solution Found = {is_solution}")