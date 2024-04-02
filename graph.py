import queue
import time


class Graph:
    def __init__(self):
        self.adj_list = {}

    def build_graph(self, edges_list, weight_selection, transport):
        for edge in edges_list:
            parts = edge.split(";")
            i = int(parts[1])
            j = int(parts[2])
            weight = float(parts[weight_selection])
            bidirectional = True
            if parts[6] == "false" and transport == "car".lower():
                bidirectional = False
            if i not in self.adj_list:
                self.adj_list[i] = []
            if j not in self.adj_list:
                self.adj_list[j] = []
            self.adj_list[i].append((j, weight))
            if bidirectional:
                self.adj_list[j].append((i, weight))

    def dijkstra(self, start, end):
        distances = {node_count: float("inf") for node_count in self.adj_list}
        predecessors = {node_count: None for node_count in self.adj_list}
        distances[start] = 0
        priority_queue = queue.PriorityQueue()
        priority_queue.put((0, start))
        start_time = time.time()
        while not priority_queue.empty():
            current_distance, current_predecessors = priority_queue.get()
            if current_predecessors == end:
                break
            if current_distance > distances[current_predecessors]:
                continue
            for neighbor, weight in self.adj_list[current_predecessors]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_predecessors
                    priority_queue.put((distance, neighbor))

        end_time = time.time()
        computation_time = end_time - start_time
        print("\nBerechnungszeit der Route: ", computation_time, "Sekunden\n")
        return distances, predecessors
