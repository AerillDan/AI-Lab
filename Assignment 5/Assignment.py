import random

# 1. Fixed random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# 2. Distance Matrix (kilometres) from the assignment dataset
DEPOT = 'A'
LOCATIONS = ['B', 'C', 'D', 'E', 'F', 'G']

DISTANCE_MATRIX = {
    'A': {'A': 0, 'B': 4, 'C': 8, 'D': 6, 'E': 7, 'F': 9, 'G': 5},
    'B': {'A': 4, 'B': 0, 'C': 5, 'D': 7, 'E': 3, 'F': 8, 'G': 6},
    'C': {'A': 8, 'B': 5, 'C': 0, 'D': 4, 'E': 6, 'F': 3, 'G': 7},
    'D': {'A': 6, 'B': 7, 'C': 4, 'D': 0, 'E': 5, 'F': 6, 'G': 8},
    'E': {'A': 7, 'B': 3, 'C': 6, 'D': 5, 'E': 0, 'F': 4, 'G': 6},
    'F': {'A': 9, 'B': 8, 'C': 3, 'D': 6, 'E': 4, 'F': 0, 'G': 5},
    'G': {'A': 5, 'B': 6, 'C': 7, 'D': 8, 'E': 6, 'F': 5, 'G': 0},
}


def calculate_route_distance(route):
    """Calculate total route distance starting and ending at depot A."""
    total_distance = DISTANCE_MATRIX[DEPOT][route[0]]  # Depot A to first location
    for i in range(len(route) - 1):
        total_distance += DISTANCE_MATRIX[route[i]][route[i + 1]]
    total_distance += DISTANCE_MATRIX[route[-1]][DEPOT]  # Last location back to Depot A
    return total_distance


def create_initial_population(pop_size, locations):
    """Create an initial population of valid random delivery routes."""
    population = []
    for _ in range(pop_size):
        route = locations[:]
        random.shuffle(route)
        population.append(route)
    return population


def tournament_selection(population, tournament_size=3):
    """Select a parent using tournament selection (shorter distance wins)."""
    competitors = random.sample(population, tournament_size)
    return min(competitors, key=calculate_route_distance)


def ordered_crossover(parent1, parent2):
    """Perform route-preserving Ordered Crossover (OX1) to avoid duplicate visits."""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    # Copy a sub-segment from parent1
    child[start:end + 1] = parent1[start:end + 1]

    # Fill remaining positions with cities from parent2 in order
    remaining = [loc for loc in parent2 if loc not in child]
    pointer = 0
    for i in range(size):
        if child[i] is None:
            child[i] = remaining[pointer]
            pointer += 1

    return child


def swap_mutation(route, mutation_rate=0.2):
    """Swap two random delivery locations in the route based on mutation rate."""
    mutated = route[:]
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(mutated)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated


def run_genetic_algorithm(
    pop_size=30,
    generations=100,
    mutation_rate=0.2,
    elitism_count=2
):
    """Run the Genetic Algorithm to find the shortest delivery route."""
    population = create_initial_population(pop_size, LOCATIONS)

    for gen in range(generations):
        # Sort population by shortest distance (best fitness first)
        population.sort(key=calculate_route_distance)

        # Elitism: carry over the top routes unchanged
        next_generation = population[:elitism_count]

        # Generate offspring to fill the rest of the new population
        while len(next_generation) < pop_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = ordered_crossover(parent1, parent2)
            child = swap_mutation(child, mutation_rate)
            next_generation.append(child)

        population = next_generation

    # Identify the best route after final generation
    best_route = min(population, key=calculate_route_distance)
    best_distance = calculate_route_distance(best_route)
    return best_route, best_distance


if __name__ == "__main__":
    best_route, best_distance = run_genetic_algorithm(
        pop_size=30,
        generations=100,
        mutation_rate=0.2,
        elitism_count=2
    )

    full_path = [DEPOT] + best_route + [DEPOT]
    print(f"Best Delivery Route: {' -> '.join(full_path)}")
    print(f"Total Distance: {best_distance} km")