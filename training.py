from canvas import Canvas
from racetrack import Track
from network import Network 
from evolution import Evolution
from storage import Storage
import os 

POPULATION_COUNT = 40 
DIMENSIONS = 5, 8, 2
MAX_GENERATIONS = 15
KEEP_COUNT = 4 
car_image_paths = [os.path.join("images", f"car{i}.png") for i in range(5)]

canvas = Canvas(Track(2), car_image_paths)


networks = [Network(DIMENSIONS) for _ in range(POPULATION_COUNT)]
evolution = Evolution(POPULATION_COUNT, KEEP_COUNT)
storage = Storage("brain.json")
best_chromosomes = storage.load()
for c, n in zip(best_chromosomes, networks):
    n.deserialise(c)

simulation_round = 1
print(f"--- Cars reached goal: {sum(n.has_reached_goal for n in networks)}")

while simulation_round <= MAX_GENERATIONS and canvas.is_simulating:

    canvas.simulate_generation(networks, simulation_round)
    simulation_round += 1
    if canvas.is_simulating:
        print(f"-- Average checkpoint reached: {sum(n.highest_checkpoint for n in networks)/len(networks):.2f}")
        print(f"---Average distance {sum(n.smallest_edge_distance for n in networks[:KEEP_COUNT]) / KEEP_COUNT:.2f}")
        print(f"--- Cars reached goal: {sum(n.has_reached_goal for n in networks)}")
        serialised = [network.serialise() for network in networks]
        offspring = evolution.execute(serialised, sum(n.has_reached_goal for n in networks))
        storage.save(offspring[:KEEP_COUNT])
        # create networks from offsprint
        networks = []
        for chromosome in offspring:
            network = Network(DIMENSIONS)
            network.deserialise(chromosome)
            networks.append(network)