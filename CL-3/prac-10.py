import numpy as np
import random

class AntColonyOptimization:
    def __init__(self, distance_matrix, num_ants=10, num_iterations=50, 
                 evaporation_rate=0.5, pheromone_constant=1.0, heuristic_constant=1.0):
        self.distance_matrix = np.array(distance_matrix)
        self.num_cities = len(distance_matrix)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = evaporation_rate
        self.pheromone_constant = pheromone_constant
        self.heuristic_constant = heuristic_constant
        
        # Initialize matrices
        self.pheromone = np.ones((self.num_cities, self.num_cities))
        self.visibility = 1 / (self.distance_matrix + np.eye(self.num_cities))
        
    def run(self):
        best_route = None
        best_distance = float('inf')
        
        for _ in range(self.num_iterations):
            ant_routes = self._construct_solutions()
            self._update_pheromones(ant_routes)
            
            # Update best solution
            for route in ant_routes:
                distance = self._calculate_route_distance(route)
                if distance < best_distance:
                    best_distance = distance
                    best_route = route
                    
        return best_route, best_distance
    
    def _construct_solutions(self):
        ant_routes = []
        for _ in range(self.num_ants):
            current_city = random.randint(0, self.num_cities - 1)
            visited = {current_city}
            route = [current_city]
            
            while len(visited) < self.num_cities:
                next_city = self._select_next_city(current_city, visited)
                route.append(next_city)
                visited.add(next_city)
                current_city = next_city
                
            ant_routes.append(route)
        return ant_routes
    
    def _select_next_city(self, current_city, visited):
        unvisited = [city for city in range(self.num_cities) if city not in visited]
        probabilities = []
        
        for city in unvisited:
            pheromone = self.pheromone[current_city][city]
            visibility = self.visibility[current_city][city]
            prob = (pheromone ** self.pheromone_constant) * (visibility ** self.heuristic_constant)
            probabilities.append((city, prob))
            
        # Select city based on probabilities
        total = sum(prob for _, prob in probabilities)
        r = random.random() * total
        cumsum = 0
        for city, prob in probabilities:
            cumsum += prob
            if cumsum >= r:
                return city
        return probabilities[-1][0]
    
    def _update_pheromones(self, ant_routes):
        delta_pheromone = np.zeros((self.num_cities, self.num_cities))
        
        for route in ant_routes:
            distance = self._calculate_route_distance(route)
            contribution = 1 / distance
            
            for i in range(len(route) - 1):
                city_a, city_b = route[i], route[i + 1]
                delta_pheromone[city_a][city_b] += contribution
                delta_pheromone[city_b][city_a] += contribution
                
        self.pheromone = (1 - self.evaporation_rate) * self.pheromone + delta_pheromone
    
    def _calculate_route_distance(self, route):
        return sum(self.distance_matrix[route[i]][route[(i + 1) % self.num_cities]] 
                  for i in range(self.num_cities))

def main():
    # Example distance matrix
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    # Create and run ACO
    aco = AntColonyOptimization(distance_matrix)
    best_route, shortest_distance = aco.run()
    
    print(f"Best route: {best_route}")
    print(f"Shortest distance: {shortest_distance}")

if __name__ == "__main__":
    main()