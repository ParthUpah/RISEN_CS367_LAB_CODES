import random
import numpy as np
from math import cos, sin, radians, sqrt, atan2

# function to calculate (total cost of the tour)
def objective_function(route, distances):
    total_cost = 0
    for i in range(len(route) - 1):
        total_cost += distances[route[i]][route[i + 1]]
    total_cost += distances[route[-1]][route[0]]  # Add the cost of returning to the starting city
    return total_cost

# function to generate a new solution by swapping two cities in the tour
def generate_new_solution(previous_solution):
    new_solution = previous_solution.copy()
    i, j = random.sample(range(len(new_solution)), 2)
    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
    return new_solution

# function to generate a random solution for the TSP
def generate_random_solution(city_count):
    route = list(range(city_count))
    random.shuffle(route)
    return route

# Function to implement the Simulated Annealing algorithm
def simulated_annealing(distance_matrix, city_count, iteration_count, initial_temp, cooling_rate):
    current_route = generate_random_solution(city_count)
    current_cost = objective_function(current_route, distance_matrix)
    best_route = current_route
    best_cost = current_cost
    temperature = initial_temp
    for iteration in range(iteration_count):
        new_route = generate_new_solution(current_route)
        new_cost = objective_function(new_route, distance_matrix)
        if new_cost < current_cost:
            current_route = new_route
            current_cost = new_cost
            if new_cost < best_cost:
                best_route = new_route
                best_cost = new_cost
        else:
            if random.random() < np.exp(-(new_cost - current_cost) / temperature):
                current_route = new_route
                current_cost = new_cost
        temperature *= cooling_rate
    return best_route, best_cost

def haversine(latitude1, longitude1, latitude2, longitude2):
    radius = 6371  # radius of earth in km
    delta_lat = radians(latitude2 - latitude1)
    delta_lon = radians(longitude2 - longitude1)
    a = sin(delta_lat / 2) * sin(delta_lat / 2) + cos(radians(latitude1)) * cos(radians(latitude2)) * sin(delta_lon / 2) * sin(delta_lon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return radius * c

# load the coordinates of the 20 important tourist locations in Rajasthan
location_coordinates = np.loadtxt('rajasthan_coordinates.txt', delimiter=',')
# calculate the pairwise distances between these locations using the Haversine formula
distance_matrix = np.zeros((20, 20))
for i in range(20):
    for j in range(i + 1, 20):
        distance_matrix[i][j] = haversine(location_coordinates[i][0], location_coordinates[i][1], location_coordinates[j][0], location_coordinates[j][1])

# Apply Simulated Annealing
initial_temp = 1000
iteration_count = 10000
cooling_rate = 0.95
optimal_route, best_cost = simulated_annealing(distance_matrix, 20, iteration_count, initial_temp, cooling_rate)

# print the optimal tour
print("Optimal Tour:")
for city in optimal_route:
    print(city)

# print the total cost of the optimal tour
print("Total Cost: ", best_cost)
