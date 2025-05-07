# PROBLEM STATEMENT:
# Implementation of Clonal selection algorithm using Python.

import numpy as np

# Define the objective function (example: sphere function)
def objective_function(x):
    return np.sum(x**2)

# Initialize parameters
num_antibodies = 20
num_generations = 100
clone_factor = 5
mutation_rate = 0.1
dimension = 5

# Initialize antibody population
antibodies = np.random.uniform(-10, 10, (num_antibodies, dimension))

# Clonal Selection Algorithm
for generation in range(num_generations):
    # Evaluate antibodies
    fitness = np.array([objective_function(antibody) for antibody in antibodies])
    
    # Select top antibodies
    top_antibodies = antibodies[np.argsort(fitness)[:int(num_antibodies/2)]]
    
    # Clone and mutate antibodies
    new_antibodies = []
    for antibody in top_antibodies:
        clones = [antibody + mutation_rate * np.random.randn(dimension) for _ in range(clone_factor)]
        new_antibodies.extend(clones)
    
    # Evaluate new antibodies
    new_fitness = np.array([objective_function(antibody) for antibody in new_antibodies])
    
    # Select the best antibodies for the next generation
    antibodies = np.array(new_antibodies)[np.argsort(new_fitness)[:num_antibodies]]

# Output the best solution found
best_antibody = antibodies[np.argmin([objective_function(antibody) for antibody in antibodies])]
print("Best solution found:", best_antibody)
print("Objective function value:", objective_function(best_antibody))
