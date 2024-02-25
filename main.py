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


# Eine Klasse für das Erstellen des Graphen erstellen
# Später noch erweitern mit Einbahnstraßen
class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edges(self, i, j, weight):
        if i not in self.adj_list:
            self.adj_list[i] = []
        if j not in self.adj_list:
            self.adj_list[j] = []
        self.adj_list[i].append((j, weight))

    def build_graph(self, edges_list):
        for edge in edges_list:
            parts = edge.split(";")
            i = int(parts[1])
            j = int(parts[2])
            weight = float(parts[4])
            self.add_edges(i, j, weight)


transp = input("Bitte wählen Sie das Transportmittel aus: Ped, Bic oder Car: ").lower()
symbols_dict_output, nodes_list_output, edges_list_output = read_file(transp)

instance_graph = Graph()
instance_graph.build_graph(edges_list_output)

print(instance_graph.adj_list)
# print(symbols_dict)
# print(nodes_list)
# print(edges_list)
