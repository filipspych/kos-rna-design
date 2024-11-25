from igraph import Graph
from convert_representation import convert_parenthesized_to_tree
from convert_representation import convert_tree_to_parenthesized
from copy import deepcopy


def create_structures_with_less_nestings(structure: str) -> [str]:
    graph = convert_parenthesized_to_tree(structure)

    pairs = find_stars_and_ends_of_nestings(graph)

    new_structures = []
    # for each pair we want to generate new graph which

    for pair in pairs:
        g = deepcopy(graph)
        child = g.neighbors(pair[0], "out")[0]
        edge_index = g.get_eid(child, g.neighbors(child, "out")[0])
        g.delete_edges(edge_index)

        for u in g.neighbors(pair[1], "out"):
            g.add_edge(child, u)

        g.vs[child]["unpaired_count_0"] = g.vs[pair[1]]["unpaired_count_0"]
        g.vs[child]["unpaired_count_1"] = g.vs[pair[1]]["unpaired_count_1"]

        # create structure for this graph
        current_str = convert_tree_to_parenthesized(g)
        new_structures.append(current_str)

    return new_structures


def find_stars_and_ends_of_nestings(g: Graph) -> [(int, int)]:
    s = []
    for v in g.neighbors(g.vs[0], "out"):
        s.append(v)

    pairs = []
    count = 0
    start = g.vs[0]
    # we
    while len(s) > 0:
        v = s.pop()

        if count > 0:
            if g.degree(v, "out") == 1 and g.vs[v]["unpaired_count_0"] == 0 and g.vs[v]["unpaired_count_1"] == 0:
                count += 1
            elif g.degree(v, "out") == 0 and count > 1:
                pairs.append((start, v))
                count = 0
            else:
                if count >= 3:
                    pairs.append((start, v))
                count = 0
        else:
            if g.degree(v, "out") == 1 and g.vs[v]["unpaired_count_0"] == 0 and g.vs[v]["unpaired_count_1"] == 0:
                count = 1
                start = v

        # after processing v go along with dfs
        for u in g.neighbors(v, "out"):
            s.append(u)

    return pairs


def create_structures_from_file(file_path: str) -> None:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    output_file_path = "DO_POROWNANIA.txt"

    with open(output_file_path, 'w') as output_file:
        for line in lines:
            print(line)
            structures = create_structures_with_less_nestings(line)
            for structure in structures:
                output_file.write(f"{line} {structure}\n")
    return


if __name__ == "__main__":
    create_structures_from_file("PROJEKTOWALNE.txt")

