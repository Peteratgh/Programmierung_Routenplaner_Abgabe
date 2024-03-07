def output(symbols_dict, edges_list, named_path, startpoint, endpoint):
    total_distance = 0
    total_time = 0
    shortest_path_streets = []

    for i in range(len(named_path) -1 ):
        current_node = named_path[i]
        next_node = named_path[i + 1]

        for edge in edges_list:
            parts = edge.split(";")
            if (int(parts[1]) == current_node and int(parts[2]) == next_node) or \
                    (int(parts[1]) == next_node and int(parts[2]) == current_node):
                distance = float(parts[4])
                time_calc = float(parts[7])

                total_distance += distance
                total_time += time_calc

                street_name = symbols_dict[int(parts[3])]
                if street_name and (not shortest_path_streets or shortest_path_streets[-1] != street_name):
                    shortest_path_streets.append(street_name)

                break

    print("\nDistanz:", round(total_distance / 1000, 2), "Kilometer")
    print("\nFahrzeit:", round(total_time, 2), "Minuten")
    print("\nKürzester Weg von :", startpoint.title(), "nach", endpoint.title(), ":", shortest_path_streets)
