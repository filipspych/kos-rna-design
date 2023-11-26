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
    pass
