from igraph import Graph
from queue import LifoQueue

# ================================================================================
# 5. Funkcja (moduł) zamieniająca reprezentację nawiasową w drzewo i vice versa
def convert_parenthesized_to_tree(parenthesized: str) -> Graph:
    """
    Konwertuje reprezentację nawiasową struktury RNA na graf.
    
    Args:
        parenthesized (str): Reprezentacja nawiasowa struktury RNA.
    ValueError: Kiedy nie da sie przekonwertowac, bo struktura jest zla
    
    Returns:
        Graph: Graf reprezentujący strukturę RNA.
    """
    # TODO: treść funkcji
    stack = LifoQueue(maxsize=len(parenthesized))
    g: Graph
    g = Graph()
    g.add_vertex()
    g.vs[0]["isPaired"] = True
    i = 0
    for char in parenthesized:
        if char == '(':
            stack.put(i)
            g.add_vertex()
            g.add_edge(i, g.vs.__len__() - 1)
            i = g.vs.__len__() - 1
            g.vs[i]["isPaired"] = True
        elif char == ')':
            if stack.empty():
                raise Exception(f"Niepoprawna reprezentacja nawiasowa: nie otwarty nawias.")
            i = stack.get()
        else:
            g.add_vertex()
            g.add_edge(i, g.vs.__len__() - 1)
            g.vs[g.vs.__len__() - 1]["isPaired"] = False
    if stack.empty == False:
        raise Exception(f"Niepoprawna reprezentacja nawiasowa: nie zamknięty nawias.")
    db = g.vs[i]["isPaired"]
    return g



def convert_tree_to_parenthesized(St: Graph) -> str:
    """
    Konwertuje graf reprezentujący strukturę RNA na reprezentację nawiasową.
    
    Args:
        St (Graph): Graf reprezentujący strukturę RNA.
    Raises:
    Returns:
        str: Reprezentacja nawiasowa struktury RNA.
    """
    # TODO: treść funkcji
    result: str = ""
    stack = LifoQueue(maxsize=len(St.vs))
    # first element is vertex number, second is vertex level in a tree
    depth = -1

    # init stack with root's children (not with root because root doesn't have parent we can skip)
    neighbors = St.neighbors(0)
    for indx in range(len(neighbors) - 1, -1, -1):
        stack.put((neighbors[indx], depth + 1))

    # DFS, adds vertex children to stack
    while not stack.empty():
        i = stack.get()

        for d in range(depth - i[1] + 1):
            result += ")"
        depth = i[1]


        if not St.vs[i[0]]["isPaired"]:
            result += "."
            depth -= 1
            continue
        result += "("

        neighbors = St.neighbors(i[0])
        for indx in range(len(neighbors) - 1, 0, -1):
            stack.put((neighbors[indx], depth + 1))

    for d in range(depth + 1):
        result += ")"

    return result
    #return result[1:(len(result) - 1)]
