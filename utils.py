from igraph import Graph

def is_structure_with_known_ND_motifs(St: Graph) -> (bool, str):
    # sprawdzanie czy struktura jest trywialnie nieprojektowalna
    for v_idx in range(St.vcount()):
        if (St.degree(v_idx, mode='all') >= 5):
            return (True, "m5 found")
        if (St.degree(v_idx, mode='all') >= 3 and any((St.vs[v_idx].attributes().get(f"unpaired_count_{i}") or 0) > 0 for i in range(St.outdegree(v_idx) + 1))):
            return (True, "m3o found")
    return False, ""

def tree_structure_to_str(St: Graph) -> str:
    ret = St.summary(1) + "\n"
    for v in St.vs:
        ret += f"Wierzchołek {v.index} (stopień: {St.degree(v, mode='all')}):" + "\n"
        for attr in v.attributes():
            ret += f"  {attr}: {v[attr]}" + "\n"
    return ret