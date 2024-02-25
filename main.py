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

transportation = input("Bitte wählen Sie das Transportmittel aus: Ped, Bic oder Car: ").lower()
symbols_dict, nodes_list, edges_list = read_file(transportation)

print(symbols_dict)
print(nodes_list)
print(edges_list)
