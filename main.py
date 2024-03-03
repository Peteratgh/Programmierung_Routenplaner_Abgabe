import sys
from graph import Graph


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
    for item in edges_list:
        parts = item.split(";")
        if int(parts[3]) == edge:
            node_from_symbol = parts[1]
            for node in nodes_list:
                if node.startswith(node_from_symbol):
                    return int(node_from_symbol)
    return None


def get_weight_index():
    while True:
        selection = input(
            "Möchten Sie den Route anhand des kürzesten Weges (distance) oder des schnellsten Weges (time) ermitteln? ").lower()
        if selection == 'exit':
            sys.exit("Das Programm wurde beendet.")
        if selection == 'distance':
            return 4
        elif selection == 'time':
            return 7
        else:
            print("Ungültige Auswahl. Bitte wählen Sie 'distance' oder 'time'.")


def output(symbols_dict, edges_list, named_path, startpoint, endpoint, weight_index):
    total_distance = 0
    shortest_path_streets = []
    for i in range(len(named_path) - 1):
        current_node = named_path[i]
        next_node = named_path[i + 1]
        for edge in edges_list:
            parts = edge.split(";")
            if (int(parts[1]) == current_node and int(parts[2]) == next_node) or \
                    (int(parts[1]) == next_node and int(parts[2]) == current_node):
                distance_or_time = float(parts[weight_index])
                total_distance += distance_or_time
                street_name = symbols_dict[int(parts[3])]
                if street_name and (not shortest_path_streets or shortest_path_streets[-1] != street_name):
                    shortest_path_streets.append(street_name)
                break

    if weight_index == 4:
        print("Kürzester Weg von: '" + startpoint.title() + "' nach '" + endpoint.title() + "' :", round(total_distance/1000, 2), "Kilometer")
    elif weight_index == 7:
        print("Kürzester Weg von: '" + startpoint.title() + "' nach '" + endpoint.title() + "' :", round(total_distance, 2), "Minuten")
    print("Kürzester Weg von : '" + startpoint.title() + "' nach '" + endpoint.title() + "' :", shortest_path_streets)


def main():
    print("Dies ist ein Routenplaner zwischen vorgegebenen Straßen der Stadt Höxter.\nEr berechnet die Entfernung"
          "zwischen zwei Straßen anhand der Distanz oder der schnellsten Fahrzeit und gibt Ihnen Die entsprechende"
          "ermittelte Dauer und Strecke aus.\nAußerdem wird der Streckenverlauf anhand der abgefahrenen Straßen angegeben.\n"
          "Sie können das Programm jederzeit mit der eingabe 'exit' beenden. Viel Spaß damit!\n")
    while True:
        transport = input("Bitte wählen Sie das Transportmittel aus: Ped, Bic oder Car: ").lower()
        if transport == 'exit':
            sys.exit("Das Programm wurde beendet.")
        elif transport not in ['ped', 'bic', 'car']:
            print("Ungültige Eingabe für Verkehrsmittel.")
        else:
            break

    symbols_dict_output, nodes_list_output, edges_list_output = read_file(transport)
    weight_index = get_weight_index()
    instance_graph = Graph()
    instance_graph.build_graph(edges_list_output, weight_index)

    while True:
        startpoint = input("Bitte geben Sie den Startpunkt ein: ").capitalize().strip().lower()
        if startpoint == 'exit':
            sys.exit("Das Programm wurde beendet.")
        elif startpoint not in map(str.lower, symbols_dict_output.values()):
            print("Ungültiger Startpunkt.")
        else:
            break

    while True:
        endpoint = input("Bitte geben Sie den Endpunkt ein: ").capitalize().strip().lower()
        if endpoint == 'exit':
            sys.exit("Das Programm wurde beendet.")
        elif endpoint not in map(str.lower, symbols_dict_output.values()):
            print("Ungültiger Endpunkt.")
        else:
            break

    start_key = find_key(symbols_dict_output, startpoint.capitalize())
    start_node = find_node(start_key, nodes_list_output, edges_list_output)
    end_key = find_key(symbols_dict_output, endpoint.capitalize())
    end_node = find_node(end_key, nodes_list_output, edges_list_output)

    distances_calc, predecessors_calc = instance_graph.dijkstra(start_node, end_node)

    shortest_path = [end_node]
    while predecessors_calc[end_node] is not None:
        end_node = predecessors_calc[end_node]
        shortest_path.insert(0, end_node)

    output(symbols_dict_output, edges_list_output, shortest_path, startpoint, endpoint, weight_index)


if __name__ == "__main__":
    main()
