# Smart Route Planner

This project is a **Smart Route Planner** built in Python. It models a weighted graph of locations and computes routes between a start and destination node.

The project demonstrates a topic taught in class: **graph algorithms (shortest path using Dijkstra's algorithm)**.

## Project Type

- Interface used: **TUI/CLI** (acceptable as per the requirement; GUI is preferred but not mandatory)
- Language: **Python**
- Paradigm: **Object-Oriented Programming (OOP)**

## Report (Included in README)

This README itself serves as the **project report**.
No separate report printout is required.

## Problem Statement

In route-planning systems, users need to find the minimum-cost path between two points in a network.
This project solves that by representing the network as a weighted undirected graph and applying shortest-path logic.

## Objectives

- Build and visualize a weighted graph of nodes and edges
- Find the optimal route between two nodes
- Compare optimal and non-optimal strategy behavior
- Validate user input for robust interaction

## Topics Used From Class

- Graph representation using an adjacency list
- Dijkstra's algorithm (single-source shortest path)
- Greedy strategy and its limitations
- Time/space trade-off with priority queue (min-heap)
- OOP design (`Graph` and `RoutePlanner` classes)

## Features Implemented

- Manual graph creation through user input
- Random graph generation (bonus feature)
- Shortest path calculation using Dijkstra
- Greedy nearest-neighbor route for comparison
- Step-by-step distance updates for Dijkstra
- Input validation for node/edge and weight entries

## Algorithms

### 1) Dijkstra's Algorithm (Primary)

- Works for non-negative edge weights
- Uses a min-heap to always expand the current least-cost node
- Guarantees shortest path when a path exists

### 2) Greedy Route (Comparison)

- Chooses the immediate smallest outgoing edge
- Faster and simple locally, but may miss the globally optimal route
- Included to show why Dijkstra is preferred

## Project Structure

- `smart_route_planner.py`: Main source file containing:
  - `Graph` class
  - `RoutePlanner` class
  - Input utility functions
  - CLI workflow (`main`)

## How to Run

1. Ensure Python 3 is installed.
2. Open terminal in the project folder.
3. Run:

```bash
python smart_route_planner.py
```

## Sample Workflow

1. Choose:
   - `1` for manual graph input, or
   - `2` for random graph generation
2. Enter start and destination nodes
3. Observe:
   - Dijkstra shortest path and total cost
   - Greedy route and cost (or failure to reach destination)
4. Read the comparison note printed at the end

## Result

The system correctly computes shortest paths using Dijkstra's algorithm and shows that greedy choices can be suboptimal.
Hence, the project successfully demonstrates practical route optimization using class-taught graph concepts.

## Constraint Compliance

- Report included in `README.md`: **Yes**
- Separate printout required: **No**
- Team members listed as contributors: **Not required / omitted**
- GUI mandatory: **No** (CLI/TUI implementation provided)
- Uses class-taught topic: **Yes (Graph + Dijkstra)**


## TEAM MEMBERS
- AP24110011559-NARAHARISETTI NAGASATYASAI SREERAM
- AP24110011551-TEJESH PUTTA
- AP24110011906-GORANTLA GOPIKRISHNA
- AP24110011660-NISANKARAO VAMSI KRISHNA
- AP24110011136-T.PRASHANTH
