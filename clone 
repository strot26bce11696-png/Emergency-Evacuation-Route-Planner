import os
from src.graph import build_graph
from src.pathfinder import dijkstra, find_nearest_safe_zone
from src.hazards import add_hazard, remove_hazard
from src.simulation import run_simulation, print_summary
from src.visualizer import plot_map
from src.storage import load_map, save_results_csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_FILE = os.path.join(BASE_DIR, "data", "map.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

data = load_map(MAP_FILE)
if data is None:
    exit()

nodes, edges, adjacency = build_graph(data)
hazards = {}
last_results = None

print("Map loaded -", len(nodes), "locations,", len(edges), "roads")


def show_map():
    print("\n--- Locations ---")
    for node_id in nodes:
        node = nodes[node_id]
        extra = ""
        if node["type"] == "safe_zone":
            extra = " (load " + str(node["load"]) + "/" + str(node["capacity"]) + ")"
        print(" ", node_id, "[" + node["type"] + "]", node["name"] + extra)

    print("\n--- Active Hazards ---")
    if not hazards:
        print("  none right now")
    for hazard_id in hazards:
        h = hazards[hazard_id]
        print(" ", hazard_id, ": centered at", h["center"], ", radius", h["radius"], ", severity", h["severity"])


def add_hazard_menu():
    hazard_id = input("Hazard id (e.g FIRE1): ").strip()
    center = input("Which node is it centered on: ").strip()
    try:
        radius = float(input("Radius: ").strip())
        severity = float(input("Severity (0 to 1): ").strip())
    except ValueError:
        print("that wasn't a valid number")
        return

    ok = add_hazard(hazards, nodes, edges, hazard_id, center, radius, severity)
    if ok:
        print("hazard added, routes will now avoid it")


def remove_hazard_menu():
    hazard_id = input("Which hazard to remove: ").strip()
    ok = remove_hazard(hazards, nodes, edges, hazard_id)
    if ok:
        print("hazard cleared")


def find_route_menu():
    start = input("Start node: ").strip()
    goal = input("Destination node (leave blank for nearest safe zone): ").strip()

    if start not in nodes:
        print("Error: no such node", start)
        return

    if goal:
        if goal not in nodes:
            print("Error: no such node", goal)
            return
        path, cost = dijkstra(nodes, edges, adjacency, start, goal)
    else:
        path, cost, goal = find_nearest_safe_zone(nodes, edges, adjacency, start)

    if path is None:
        print("Error: no route found")
        return

    print("\nRoute found (" + str(len(path)) + " stops, cost " + str(round(cost, 1)) + "):")
    print("  " + " -> ".join(path))
    save_path = plot_map(nodes, edges, route=path, hazards=hazards, title=start + " to " + goal,
                          save_path=os.path.join(OUTPUT_DIR, "route.png"))
    print("map saved to", save_path)


def run_simulation_menu():
    global last_results
    print("Enter each source building and how many people are there.")
    print("Leave the node id blank when you're done.")
    sources = {}
    while True:
        node_id = input("  Node id: ").strip()
        if not node_id:
            break
        try:
            sources[node_id] = int(input("  People there: ").strip())
        except ValueError:
            print("  not a valid number, skipping that one")

    if not sources:
        print("nothing entered")
        return

    results, unassigned = run_simulation(nodes, edges, adjacency, sources)
    last_results = results
    print()
    print_summary(results, unassigned)


def visualize_menu():
    save_path = plot_map(nodes, edges, hazards=hazards, save_path=os.path.join(OUTPUT_DIR, "city_map.png"))
    print("map saved to", save_path)


def export_csv_menu():
    if not last_results:
        print("run a simulation first (option 5)")
        return
    out_path = os.path.join(OUTPUT_DIR, "simulation_results.csv")
    save_results_csv(last_results, out_path)
    print("saved to", out_path)


MENU = """
========================================
 Emergency Evacuation Route Planner
========================================
 1. Show map and hazards
 2. Add a hazard
 3. Remove a hazard
 4. Find a route
 5. Run evacuation simulation
 6. Save a picture of the map
 7. Export last simulation to csv
 0. Quit
========================================
"""

while True:
    print(MENU)
    choice = input("Pick an option: ").strip()
    if choice == "0":
        print("Bye, stay safe!")
        break
    elif choice == "1":
        show_map()
    elif choice == "2":
        add_hazard_menu()
    elif choice == "3":
        remove_hazard_menu()
    elif choice == "4":
        find_route_menu()
    elif choice == "5":
        run_simulation_menu()
    elif choice == "6":
        visualize_menu()
    elif choice == "7":
        export_csv_menu()
    else:
        print("not a valid option, try again")