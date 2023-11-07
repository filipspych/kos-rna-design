from igraph import Graph

def is_tree_representation_correct(St: Graph) -> (bool, str):
    # sprawdzanie czy struktura jest trywialnie nieprojektowalna
    for v in map(lambda visited: St.vs[visited[0]], St.dfs(0)):
        if (St.degree(v) == 5):
            return (False, "m5 found")
        if (St.degree(v) >= 3 and any(v[f"unpaired_count_{i}"] > 0 for i in range(St.outdegree(v)))):
            return (False, "m3o found")
    return True, ""

def tree_structure_to_str(St: Graph) -> str:
    ret = St.summary(1) + "\n"
    for v in St.vs:
        ret += f"Wierzchołek {v.index}:" + "\n"
        for attr in v.attributes():
            ret += f"  {attr}: {v[attr]}" + "\n"
    return ret