import sys
from graph import Graph
from data_processing import read_file, find_key, find_node, get_weight_index


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
    print("Willkommen zum Routenplaner!\n""\n"
          "Dieses Programm ermöglicht es Ihnen, die Entfernung zwischen zwei vorgegebenen Straßen basierend auf der Distanz oder der schnellsten Fahrzeit zu berechnen.\n"
          "Sie erhalten die entsprechende ermittelte Dauer und Strecke.\n"
          "Darüber hinaus wird Ihnen der Streckenverlauf anhand der abgefahrenen Straßen angezeigt.\n"
          "Zum Beenden des Programms können Sie jederzeit die Eingabe 'exit' verwenden.\n""\n"
          "Viel Spaß beim Nutzen des Routenplaners! \n")
    while True:
        city = input("Möchten Sie auf Daten für Rostock oder Höxter zugreifen? ").lower()
        transport = input("Bitte wählen Sie das Transportmittel aus: Ped, Bic oder Car: ").lower()
        if transport == 'exit':
            sys.exit("Das Programm wurde beendet.")
        elif transport not in ['ped', 'bic', 'car']:
            print("Ungültige Eingabe für Verkehrsmittel.")
        else:
            break
    symbols_dict_output, nodes_list_output, edges_list_output = read_file(city, transport)
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
