import os
from src.graph import build_graph
from src.pathfinder import dijkstra
from src.hazards import add_hazard
from src.simulation import run_simulation, print_summary
from src.visualizer import plot_map
from src.storage import load_map, save_results_csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_FILE = os.path.join(BASE_DIR, "data", "map.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

data = load_map(MAP_FILE)
nodes, edges, adjacency = build_graph(data)
hazards = {}

print("Generating sample outputs...")

plot_map(nodes, edges, title="City Map (no hazards)",
          save_path=os.path.join(OUTPUT_DIR, "1_city_map.png"))

path, cost = dijkstra(nodes, edges, adjacency, "B1", "S2")
plot_map(nodes, edges, route=path, title="Route: B1 to S2 (before hazard)",
          save_path=os.path.join(OUTPUT_DIR, "2_route_before_hazard.png"))

add_hazard(hazards, nodes, edges, "FIRE1", "I1", 8, 0.9)
plot_map(nodes, edges, hazards=hazards, title="City Map with Hazard (FIRE1 at I1)",
          save_path=os.path.join(OUTPUT_DIR, "3_city_map_with_hazard.png"))

path2, cost2 = dijkstra(nodes, edges, adjacency, "B1", "S2")
plot_map(nodes, edges, route=path2, hazards=hazards, title="Route: B1 to S2 (after hazard, rerouted)",
          save_path=os.path.join(OUTPUT_DIR, "4_route_after_hazard.png"))

sources = {"B1": 150, "B2": 400}
results, unassigned = run_simulation(nodes, edges, adjacency, sources)
save_results_csv(results, os.path.join(OUTPUT_DIR, "5_simulation_results.csv"))

print()
print_summary(results, unassigned)
print()
print("Route before hazard:", path, "cost", round(cost, 1))
print("Route after hazard: ", path2, "cost", round(cost2, 1))
print()
print("All sample outputs saved in the output folder.")