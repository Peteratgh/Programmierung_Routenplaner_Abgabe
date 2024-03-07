import simplekml


def export_kml(nodes_list, shortest_path, startpoint, endpoint, weight_selection):

    kml = simplekml.Kml()
    for node in nodes_list:
        if node.startswith("#"):
            continue

    polygon_coordinates = []
    for node_id in shortest_path:
        for node in nodes_list:
            if node.startswith("#"):
                continue

            parts = node.split(";")
            if int(parts[0]) == node_id:
                node_coordinates = (float(parts[2]), float(parts[1]))
                polygon_coordinates.append(node_coordinates)
                break

    kml.newlinestring(name="Kürzester Weg", coords=polygon_coordinates)

    if weight_selection == 7:
        print("\nKML-Datei wurde erfolgreich exportiert: Schnellste Route von: " + startpoint.title() + " nach " + endpoint.title() + ".kml")
        kml.save("Karten/Schnellste Route von " + startpoint.title() + " nach " + endpoint.title() + ".kml")
    elif weight_selection == 4:
        print("\nKML-Datei wurde erfolgreich exportiert: Kürzeste Route von: " + startpoint.title() + " nach " + endpoint.title() + ".kml")
        kml.save("Karten/Kürzeste Route von " + startpoint.title() + " nach " + endpoint.title() + ".kml")
