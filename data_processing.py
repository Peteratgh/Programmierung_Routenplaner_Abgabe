import sys


def read_file(city, transportation):
    symbols_dict = {}
    nodes_list = []
    edges_list = []

    if city.lower() == "rostock":
        if transportation == "ped":
            dateiquelle = "Daten/rostock_PED.txt"
        elif transportation == "bic":
            dateiquelle = "Daten/rostock_BIC.txt"
        elif transportation == "car":
            dateiquelle = "Daten/rostock_CAR.txt"
        else:
            print("Ungültige Eingabe für Verkehrsmittel.")
            return symbols_dict, nodes_list, edges_list
    elif city.lower() == "höxter":
        if transportation == "ped":
            dateiquelle = "Daten/hoexter_full_PED.txt"
        elif transportation == "bic":
            dateiquelle = "Daten/hoexter_full_BIC.txt"
        elif transportation == "car":
            dateiquelle = "Daten/hoexter_full_CAR.txt"
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
                    parts = line.split(";")
                    distance = float(parts[4])
                    speed = float(parts[5])
                    duration = round(distance / speed / 10, 6)
                    updated_edge = ";".join(parts[:7]) + ";" + str(duration)
                    edges_list.append(updated_edge)

    return symbols_dict, nodes_list, edges_list


def find_key(dictionary, search_node):
    for a, b in dictionary.items():
        if b.casefold() == search_node.casefold():
            return a
    return None


def find_node(edge, nodes_list, edges_list):
    matching_edges = []
    for item in edges_list:
        parts = item.split(";")
        if int(parts[3]) == edge:
            matching_edges.append(item)

    middle_index = len(matching_edges) // 2
    if middle_index < len(matching_edges):
        middle_edge = matching_edges[middle_index]
        parts = middle_edge.split(";")
        node_from_symbol = parts[1]
        for node in nodes_list:
            if node.startswith(node_from_symbol):
                return int(node_from_symbol)

    return None


def get_weight_index():
    while True:
        selection = input(
            "Möchten Sie den Route anhand des kürzesten Weges (distance) oder des schnellsten Weges (time) ermitteln? "
        ).lower()
        if selection == "exit":
            sys.exit("Das Programm wurde beendet.")
        if selection == "distance":
            return 4
        elif selection == "time":
            return 7
        else:
            print("Ungültige Auswahl. Bitte wählen Sie 'distance' oder 'time'.")
