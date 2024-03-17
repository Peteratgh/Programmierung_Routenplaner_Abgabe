from math import radians, degrees, atan2, sin, cos


def get_direction(origin_lat, origin_lon, target_lat, target_lon):
    lat1, lon1, lat2, lon2 = map(
        radians, [origin_lat, origin_lon, target_lat, target_lon]
    )
    d_lon = lon2 - lon1
    y = sin(d_lon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(d_lon)
    angle_direction = degrees(atan2(y, x))
    calc_direction = (angle_direction + 360) % 360
    return calc_direction


def direction(nodes_list, last_node, current_node, next_node):
    previous_direction = get_direction(
        *map(float, nodes_list[last_node].split(";")[1:]),
        *map(float, nodes_list[current_node].split(";")[1:]),
    )
    current_direction = get_direction(
        *map(float, nodes_list[current_node].split(";")[1:]),
        *map(float, nodes_list[next_node].split(";")[1:]),
    )
    angle = previous_direction - current_direction

    directions = ["N", "NO", "O", "SO", "S", "SW", "W", "NW", "N"]

    index = int((current_direction + 22.5) / 45)

    if -45 <= angle <= 45:
        out = "geradeaus"
    elif -45 >= angle >= -135 or 225 <= angle <= 315:
        out = "rechts"
    else:
        out = "links"

    return out, directions[index]


def output(
    symbols_dict, edges_list, shortest_path_nodes, nodes_list, startpoint, endpoint
):
    total_distance = 0
    total_time = 0
    prev_street = None
    intermediate_distance = 0
    last_node = 0
    out, himmel = direction(
        nodes_list, last_node, shortest_path_nodes[0], shortest_path_nodes[1]
    )
    print("Route von " + startpoint.title() + " nach " + endpoint.title() + ":\n")
    print("Fahren Sie Richtung " + himmel)
    for i in range(len(shortest_path_nodes) - 1):
        current_node = shortest_path_nodes[i]
        next_node = shortest_path_nodes[i + 1]

        for edge in edges_list:
            parts = edge.split(";")
            if (int(parts[1]) == current_node and int(parts[2]) == next_node) or (
                int(parts[1]) == next_node and int(parts[2]) == current_node
            ):
                distance = float(parts[4])
                time_calc = float(parts[7])

                total_distance += distance
                total_time += time_calc

                street_name = symbols_dict[int(parts[3])]
                if street_name == "":
                    street_name = "Unbekannte Straße"

                if street_name != prev_street:
                    if prev_street is not None:
                        out, himmel = direction(
                            nodes_list, last_node, current_node, next_node
                        )

                        print(
                            "Nach "
                            + str(int(intermediate_distance))
                            + " m "
                            + out
                            + " auf "
                            + street_name
                        )

                    intermediate_distance = 0
                    prev_street = street_name
                last_node = current_node
                intermediate_distance += distance

                break

    print("Nach " + str(int(intermediate_distance)) + " m haben Sie Ihr Ziel erreicht!")
    print("\nDistanz:", round(total_distance / 1000, 2), "Kilometer")
    print("\nFahrzeit:", round(total_time, 2), "Minuten")
