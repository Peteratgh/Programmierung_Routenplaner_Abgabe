import sys
import time

from data_processing import read_file, find_key, find_node, get_weight_index
from export_kml import export_kml
from graph import Graph
from output import output


def main(restart="n"):
    if restart == "n":
        print(
            "Willkommen zum Routenplaner!\n"
            "\n"
            "Dieses Programm ermöglicht es Ihnen, die Entfernung zwischen zwei vorgegebenen Straßen basierend auf der Distanz oder der schnellsten Fahrzeit zu berechnen.\n"
            "Sie erhalten die entsprechende ermittelte Dauer und Strecke.\n"
            "Darüber hinaus wird Ihnen der Streckenverlauf anhand der abgefahrenen Straßen angezeigt.\n"
            "Zum Beenden des Programms können Sie jederzeit die Eingabe 'exit' verwenden.\n"
            "\n"
            "Viel Spaß beim Nutzen des Routenplaners!\n"
        )
    while True:
        city = input(
            "Möchten Sie auf Daten für Rostock oder Höxter zugreifen? "
        ).lower()
        if city == "exit":
            sys.exit("Das Programm wurde beendet.")
        elif city not in ["rostock", "höxter"]:
            print("Ungültige Eingabe für die Stadt.")
        else:
            break
    while True:
        transport = input(
            "Bitte wählen Sie das Transportmittel aus: Ped, Bic oder Car: "
        ).lower()
        if transport == "exit":
            sys.exit("Das Programm wurde beendet.")
        elif transport not in ["ped", "bic", "car"]:
            print("Ungültige Eingabe für Verkehrsmittel.")
        else:
            break

    symbols_dict_output, nodes_list_output, edges_list_output = read_file(
        city, transport
    )
    weight_index = get_weight_index()
    instance_graph = Graph()
    instance_graph.build_graph(edges_list_output, weight_index, transport)

    while True:
        startpoint = (
            input("Bitte geben Sie den Startpunkt ein: ").capitalize().strip().lower()
        )
        if startpoint == "exit":
            sys.exit("Das Programm wurde beendet.")
        elif startpoint not in map(str.lower, symbols_dict_output.values()):
            print("Ungültiger Startpunkt.")
        else:
            break

    while True:
        endpoint = (
            input("Bitte geben Sie den Endpunkt ein: ").capitalize().strip().lower()
        )
        if endpoint == "exit":
            sys.exit("Das Programm wurde beendet.")
        elif endpoint not in map(str.lower, symbols_dict_output.values()):
            print("Ungültiger Endpunkt.")
        else:
            break
    start_time_main = time.time()
    start_key = find_key(symbols_dict_output, startpoint.capitalize())
    start_node = find_node(start_key, nodes_list_output, edges_list_output)
    end_key = find_key(symbols_dict_output, endpoint.capitalize())
    end_node = find_node(end_key, nodes_list_output, edges_list_output)

    distances_calc, predecessors_calc = instance_graph.dijkstra(start_node, end_node)

    shortest_path = [end_node]
    while predecessors_calc[end_node] is not None:
        end_node = predecessors_calc[end_node]
        shortest_path.insert(0, end_node)

    output(
        symbols_dict_output,
        edges_list_output,
        shortest_path,
        nodes_list_output,
        startpoint,
        endpoint,
    )
    kml_request = input("Möchten Sie die Route als KML-Datei exportieren?[y/n] ")

    end_time_main = time.time()
    computation_time_main = end_time_main - start_time_main

    if kml_request == "y":
        export_kml(nodes_list_output, shortest_path, startpoint, endpoint, weight_index)

    print(
        "\nAusführungszeit des Programms(Benutzereingaben ausgenommen): ",
        computation_time_main,
        "Sekunden\n",
    )

    restart = input("Möchten Sie einen neuen Durchlauf starten?[y/n] ")
    print("\n")

    if restart == "y":
        main(restart)
    else:
        print("Vielen Dank für das Nutzen des Routenplaners")


if __name__ == "__main__":
    main()
