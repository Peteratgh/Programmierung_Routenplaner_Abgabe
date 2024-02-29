import queue


def read_file(transportation):
    symbols_dict = {}
    nodes_list = []
    edges_list = []

    if transportation == "ped":
        dateiquelle = "hoexter_full_PED.txt"
    elif transportation == "bic":
        dateiquelle = "hoexter_full_BIC.txt"
    elif transportation == "car":
        dateiquelle = "hoexter_full_CAR.txt"
    else:
        print("Ungültige Eingabe für Verkehrsmittel.")
        return symbols_dict, nodes_list, edges_list

    with open(dateiquelle, "r", encoding="UTF-8") as file:
        current_selection = None
        for line in file:
            line = line.strip()
            if line.startswith("# Section: Symbols"):
                current_selection = "symbols"
            elif line.startswith("# Section: Nodes"):
                current_selection = "nodes"
            elif line.startswith("# Section: Edges"):
                current_selection = "edges"
            else:
                if current_selection == "symbols":
                    parts = line.split(";")
                    if len(parts) >= 2:
                        symbols_dict[int(parts[0])] = parts[1]
                elif current_selection == "nodes":
                    nodes_list.append(line)
                elif current_selection == "edges":
                    edges_list.append(line)

    return symbols_dict, nodes_list, edges_list


def find_key(dictionary, search_node):
    for a, b in dictionary.items():
        if b == search_node:
            print("find_key Zwischenergebnis:", a)
            return a
    return None


def find_node(edge, nodes_list, edges_list):
    for item in edges_list:
        parts = item.split(";")
        if int(parts[3]) == edge:
            node_from_symbol = parts[1]
            for node in nodes_list:
                if node.startswith(node_from_symbol):
                    print("find_node Zwischenergebnis:", node)
                    return int(node_from_symbol)
    return None


class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edges(self, i, j, weight):
        if i not in self.adj_list:
            self.adj_list[i] = []
        if j not in self.adj_list:
            self.adj_list[j] = []
        self.adj_list[i].append((j, weight))
        self.adj_list[j].append((i, weight))

    def build_graph(self, edges_list):
        for edge in edges_list:
            parts = edge.split(";")
            i = int(parts[1])
            j = int(parts[2])
            weight = float(parts[4])
            self.add_edges(i, j, weight)

    def dijkstra(self, start, end):
        distances = {}
        for node_count in self.adj_list:
            distances[node_count] = float("inf")
        predecessors = {}
        for node_count in self.adj_list:
            predecessors[node_count] = None
        distances[start] = 0
        priority_queue = queue.PriorityQueue()
        priority_queue.put((0, start))

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

        return distances, predecessors


transport = input("Bitte wählen Sie das Transportmittel aus: Ped, Bic oder Car: ").lower()
symbols_dict_output, nodes_list_output, edges_list_output = read_file(transport)

instance_graph = Graph()
instance_graph.build_graph(edges_list_output)

start_node = int(input("Bitte geben Sie den Startknoten ein: "))
end_node = int(input("Bitte geben Sie den Zielknoten ein: "))

distances_calc, predecessors_calc = instance_graph.dijkstra(start_node, end_node)

shortest_path = [end_node]
while predecessors_calc[end_node] is not None:
    end_node = predecessors_calc[end_node]
    shortest_path.insert(0, end_node)

distance_between_nodes = distances_calc[shortest_path[-1]]

print("Kürzester Pfad von " + str(start_node) + " nach " + str(shortest_path[-1]) + ": " + str(shortest_path))
print("Entfernung zwischen " + str(start_node) + " und " + str(shortest_path[-1]) + ": " + str(distance_between_nodes))

# instance_graph.adj_list
# print(symbols_dict)
# print(nodes_list)
# print(edges_list)
