"""
Smart Route Planner (CLI, OOP)

This project demonstrates shortest-path planning with:
1) Dijkstra's algorithm (primary and optimal for non-negative weights)
2) A Greedy nearest-neighbor strategy (comparison only, may be suboptimal)
"""

from __future__ import annotations

import heapq
import random
from typing import Dict, List, Optional, Set, Tuple


class Graph:
    """Represents a weighted, undirected graph using an adjacency list."""

    def __init__(self) -> None:
        """Initialize an empty graph."""
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node: str) -> None:
        """Add a node if it does not already exist."""
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """
        Add an undirected edge between u and v with a non-negative weight.

        Args:
            u: Source node.
            v: Destination node.
            weight: Edge weight (must be >= 0 for Dijkstra).
        """
        if weight < 0:
            raise ValueError("Negative weights are not supported by Dijkstra.")

        self.add_node(u)
        self.add_node(v)

        self.adjacency[u].append((v, weight))
        self.adjacency[v].append((u, weight))

    def get_nodes(self) -> List[str]:
        """Return all nodes in sorted order."""
        return sorted(self.adjacency.keys())

    def has_node(self, node: str) -> bool:
        """Check whether a node exists in the graph."""
        return node in self.adjacency

    def neighbors(self, node: str) -> List[Tuple[str, float]]:
        """Return neighbors of a node."""
        return self.adjacency.get(node, [])

    def display_graph(self) -> None:
        """Print the adjacency list representation of the graph."""
        print("\nGraph (Adjacency List):")
        if not self.adjacency:
            print("  [Empty graph]")
            return

        for node in self.get_nodes():
            neighbors_str = ", ".join(
                f"{neighbor}(w={weight})" for neighbor, weight in self.adjacency[node]
            )
            print(f"  {node} -> {neighbors_str if neighbors_str else 'No connections'}")


class RoutePlanner:
    """Runs route-planning algorithms on a Graph object."""

    def __init__(self, graph: Graph) -> None:
        """
        Initialize planner with a graph.

        Args:
            graph: Graph object containing nodes and weighted edges.
        """
        self.graph = graph

    def get_path(self, parent: Dict[str, Optional[str]], end: str) -> List[str]:
        """
        Reconstruct path from parent map.

        Args:
            parent: Dictionary storing parent pointers.
            end: Destination node.

        Returns:
            List of nodes from source to destination.
        """
        path: List[str] = []
        current: Optional[str] = end
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        return path

    def dijkstra(
        self, start: str, end: str, show_steps: bool = True
    ) -> Tuple[List[str], float]:
        """
        Compute shortest path from start to end using Dijkstra's algorithm.

        How it works:
        - Maintains the current best known distance to each node.
        - Uses a min-heap priority queue to always expand the node with the
          smallest tentative distance first.
        - Relaxes neighboring edges and updates distances when a shorter path
          is found.

        Args:
            start: Start node.
            end: Destination node.
            show_steps: If True, prints distance updates during execution.

        Returns:
            (path, total_cost). If no path exists, returns ([], inf).
        """
        if not self.graph.has_node(start) or not self.graph.has_node(end):
            return [], float("inf")

        nodes = self.graph.get_nodes()
        dist: Dict[str, float] = {node: float("inf") for node in nodes}
        parent: Dict[str, Optional[str]] = {node: None for node in nodes}
        dist[start] = 0.0

        # Priority queue stores (distance_so_far, node)
        priority_queue: List[Tuple[float, str]] = [(0.0, start)]
        visited: Set[str] = set()

        if show_steps:
            print("\n[Dijkstra] Step-by-step distance updates:")

        while priority_queue:
            current_dist, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            if show_steps:
                print(f"  Visiting {current_node} with current distance {current_dist}")

            if current_node == end:
                break

            for neighbor, weight in self.graph.neighbors(current_node):
                if neighbor in visited:
                    continue

                new_dist = current_dist + weight
                if new_dist < dist[neighbor]:
                    old_dist = dist[neighbor]
                    dist[neighbor] = new_dist
                    parent[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_dist, neighbor))

                    if show_steps:
                        print(
                            f"    Update: {neighbor} distance "
                            f"{old_dist} -> {new_dist} via {current_node}"
                        )

        if dist[end] == float("inf"):
            return [], float("inf")

        return self.get_path(parent, end), dist[end]

    def greedy_route(self, start: str, end: Optional[str] = None) -> Tuple[List[str], float]:
        """
        Build a route by greedily selecting the nearest unvisited neighbor.

        Why this may fail:
        - Greedy chooses the best immediate (local) step.
        - It does not consider global future consequences.
        - Therefore, it can get trapped in suboptimal paths compared to Dijkstra.

        Args:
            start: Start node.
            end: Optional destination. If provided, stop when destination reached.
                 If None, attempts to visit as many reachable nodes as possible.

        Returns:
            (route, total_cost). If movement is impossible, returns ([start], 0)
            for valid start or ([], inf) for invalid start.
        """
        if not self.graph.has_node(start):
            return [], float("inf")
        if end is not None and not self.graph.has_node(end):
            return [], float("inf")

        route = [start]
        total_cost = 0.0
        visited: Set[str] = {start}
        current = start

        while True:
            if end is not None and current == end:
                break

            candidates = [
                (weight, neighbor)
                for neighbor, weight in self.graph.neighbors(current)
                if neighbor not in visited
            ]

            if not candidates:
                # No unvisited neighbor left from current node.
                break

            # Greedy step: pick edge with minimum immediate cost.
            weight, next_node = min(candidates)
            visited.add(next_node)
            route.append(next_node)
            total_cost += weight
            current = next_node

        return route, total_cost


def _read_positive_int(prompt: str) -> int:
    """Read a positive integer from user input with validation."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value <= 0:
                print("Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def _read_non_negative_float(prompt: str) -> float:
    """Read a non-negative float from user input with validation."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < 0:
                print("Weight must be non-negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def build_graph_from_input() -> Graph:
    """Build graph manually by reading nodes and edges from user."""
    graph = Graph()

    node_count = _read_positive_int("Enter number of nodes: ")
    print("Enter node names (example: A, B, City1):")
    for i in range(node_count):
        while True:
            node_name = input(f"  Node {i + 1}: ").strip()
            if not node_name:
                print("Node name cannot be empty.")
                continue
            if graph.has_node(node_name):
                print("Node already exists. Enter a unique node name.")
                continue
            graph.add_node(node_name)
            break

    edge_count = _read_positive_int("Enter number of edges: ")
    print("\nEnter each edge in format: source destination weight")
    for i in range(edge_count):
        while True:
            edge_input = input(f"  Edge {i + 1}: ").strip().split()
            if len(edge_input) != 3:
                print("Invalid format. Use: source destination weight")
                continue

            u, v, w_raw = edge_input
            if not graph.has_node(u) or not graph.has_node(v):
                print("Invalid nodes. Please use existing node names.")
                continue

            try:
                weight = float(w_raw)
                if weight < 0:
                    print("Weight must be non-negative.")
                    continue
            except ValueError:
                print("Weight must be numeric.")
                continue

            graph.add_edge(u, v, weight)
            break

    return graph


def generate_random_graph() -> Graph:
    """
    Bonus feature:
    Generate a random connected-ish graph with user-provided size and weights.
    """
    graph = Graph()
    node_count = _read_positive_int("Enter number of nodes to generate: ")
    extra_edges = _read_positive_int("Enter number of extra random edges: ")
    max_weight = _read_non_negative_float("Enter maximum edge weight: ")
    if max_weight == 0:
        max_weight = 1.0

    nodes = [f"N{i + 1}" for i in range(node_count)]
    for n in nodes:
        graph.add_node(n)

    # Create a base chain so most nodes are reachable.
    for i in range(node_count - 1):
        w = round(random.uniform(1, max_weight), 2)
        graph.add_edge(nodes[i], nodes[i + 1], w)

    # Add extra random edges.
    for _ in range(extra_edges):
        u, v = random.sample(nodes, 2)
        w = round(random.uniform(1, max_weight), 2)
        graph.add_edge(u, v, w)

    print("\nRandom graph generated successfully.")
    return graph


def _read_existing_node(prompt: str, graph: Graph) -> str:
    """Read a node name and ensure it exists in the graph."""
    while True:
        node = input(prompt).strip()
        if graph.has_node(node):
            return node
        print("Node not found. Please enter a valid node from the graph.")


def format_route(route: List[str]) -> str:
    """Format route list as A -> B -> C string."""
    return " -> ".join(route)


def run_planner(graph: Graph) -> None:
    """Execute route-planning workflow for a given graph."""
    graph.display_graph()
    planner = RoutePlanner(graph)

    print("\nAvailable nodes:", ", ".join(graph.get_nodes()))
    start = _read_existing_node("Enter start node: ", graph)
    end = _read_existing_node("Enter destination node: ", graph)

    dijkstra_path, dijkstra_cost = planner.dijkstra(start, end, show_steps=True)
    greedy_path, greedy_cost = planner.greedy_route(start, end=end)

    print("\n--- Results ---")
    if dijkstra_path:
        print(f"Shortest Path (Dijkstra): {format_route(dijkstra_path)}")
        print(f"Total Cost (Dijkstra): {dijkstra_cost}")
    else:
        print("Shortest Path (Dijkstra): No path found")
        print("Total Cost (Dijkstra): Infinity")

    if greedy_path and greedy_path[-1] == end:
        print(f"Greedy Route: {format_route(greedy_path)}")
        print(f"Total Cost (Greedy): {greedy_cost}")
    elif greedy_path:
        print(f"Greedy Route: {format_route(greedy_path)}")
        print("Total Cost (Greedy): Could not reach destination")
    else:
        print("Greedy Route: No route found")
        print("Total Cost (Greedy): Infinity")

    print("\nComparison Note:")
    print(
        "Dijkstra guarantees the shortest path (for non-negative weights), "
        "while Greedy may choose a locally cheap edge that leads to a costlier route."
    )


def main() -> None:
    """Main CLI entry point."""
    print("=== Smart Route Planner ===")
    print("1) Build graph manually")
    print("2) Generate random graph (bonus)")

    choice = ""
    while choice not in {"1", "2"}:
        choice = input("Choose an option (1 or 2): ").strip()
        if choice not in {"1", "2"}:
            print("Invalid option. Please choose 1 or 2.")

    if choice == "1":
        graph = build_graph_from_input()
    else:
        graph = generate_random_graph()

    run_planner(graph)


if __name__ == "__main__":
    main()
