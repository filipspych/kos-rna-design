from queue import LifoQueue
import igraph as ig
from igraph import Graph

from utils import is_structure_with_known_ND_motifs, tree_structure_to_str

# ================================================================================
# 5. Funkcja (moduł) zamieniająca reprezentację nawiasową w drzewo i vice versa
def convert_parenthesized_to_tree(parenthesized: str) -> Graph:
    """
    Konwertuje reprezentację nawiasową struktury RNA na graf.
    
    Args:
        parenthesized (str): Reprezentacja nawiasowa struktury RNA.
    Raises:
        ValueError: Kiedy nie da sie przekonwertowac, bo struktura nawiasów jest zla
    Returns:
        Graph: Graf reprezentujący strukturę RNA. 
        Struktura tego grafu jest opisana w README.md
    """
    g = ig.Graph(directed=True)
    v = g.add_vertex(is_root=True, unpaired_count_0=0, unpaired_count_1=0, unpaired_count_2=0)
    opened_parentheses_count = 0

    for c in parenthesized:
        if c == ".":
            v[f"unpaired_count_{v.outdegree()}"] = (v.attributes().get(f"unpaired_count_{v.outdegree()}") or 0) + 1
        if c == "(":
            opened_parentheses_count += 1
            v_prev = v
            v = g.add_vertex(is_root=False, unpaired_count_0=0, unpaired_count_1=0)
            g.add_edge(v_prev, v)
        if c == ")":
            opened_parentheses_count -= 1
            if (len(g.predecessors(v)) == 0):
                raise ValueError("Unopened parenthesis")
            v = g.vs[g.predecessors(v)[0]]
    
    if opened_parentheses_count != 0:
        raise ValueError("Unclosed parenthesis")
    return g


def convert_tree_to_parenthesized(St: Graph) -> str:
    """
    Konwertuje graf reprezentujący strukturę RNA na reprezentację nawiasową.
    Rozpoczyna konwersję od wierzchołka oznaczonego jako root 
    własnością is_root=True.
    
    Args:
        St (Graph): Graf reprezentujący strukturę RNA.
    Raises:
    Returns:
        str: Reprezentacja nawiasowa struktury RNA.
    """
    return convert_subtree_to_parenthesized(St, St.vs.find(is_root=True).index)

def convert_subtree_to_parenthesized(St: Graph, rootIdx: int) -> str:
    """
    Konwertuje graf reprezentujący strukturę RNA na reprezentację nawiasową.
    
    Args:
        St (Graph): Graf reprezentujący strukturę RNA.
        rootIdx (int): indeks od którego zaczniemy wypisywanie
    Raises:
    Returns:
        str: Reprezentacja nawiasowa struktury RNA.
    """
    parenthesized = ""
    v = St.vs[rootIdx]
    parenthesized += "."*v[f"unpaired_count_0"]

    vs_idx = St.successors(v)
    i = 1
    for v_idx in vs_idx:
        parenthesized += "("
        parenthesized += convert_subtree_to_parenthesized(St, v_idx)
        parenthesized += ")"
        parent = St.vs[v_idx].predecessors()[0]
        parenthesized += "."*(parent.attributes().get(f"unpaired_count_{i}") or 0)
        i += 1

    return parenthesized

def convert_parenthesized_to_naive_tree(parenthesized: str) -> Graph:
    """
    Konwertuje reprezentację nawiasową struktury RNA na naiwnie zbudowany graf,
    gdzie niesparowane wierzchołki są reprezentowane jako wierzchołki w grafie 
    (a nie jako liczba całkowita).
    
    Args:
        parenthesized (str): Reprezentacja nawiasowa struktury RNA.
    ValueError: Kiedy nie da sie przekonwertowac, bo struktura jest zla
    
    Returns:
        Graph: Graf reprezentujący naiwnie strukturę RNA.
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

def convert_parenthesized_to_numberized(parenthesized: str) -> str:
    """
    Zamiast kropek wstawia liczby, które oznaczają ile kropek jest w grupie.
    """
    count = 0
    result = ""
    for char in parenthesized:
        if char == '.':
            count += 1
        else:
            if count > 0:
                result += str(count)
                count = 0
            result += char
    if count > 0:
        result += str(count)
    return result
    

if __name__ == "__main__":
    print("Unit testy")

    # Lista różnych reprezentacji nawiasowych drzew do przetestowania
    data = [
        "()()().",          
        "..(...).",        
        "(..)",              # Proste drzewo binarne
        "((.)..)",           # Drzewo binarne z jednym dzieckiem
        "((..)(..))",        # Pełne drzewo binarne
        "(((..).).)",        # Niesymetryczne drzewo binarne
        ""                   # Puste drzewo
    ]

    # Pętla przechodząca przez wszystkie przykłady
    for expected in data:
        print(expected)
        St = convert_parenthesized_to_tree(expected)
        print("Po konwersji na drzewo:")
        print(tree_structure_to_str(St))
        actual = convert_tree_to_parenthesized(St)
        print("Powrót do reprezentacji nawiasowej:", actual)
        print("Czy reprezentacja jest trywialnie ND:", is_structure_with_known_ND_motifs(St))
        print("\n")  # Dodanie pustej linii dla czytelności
        assert expected == actual, f"Błąd w konwersji. Przed konwersją: {expected}, po konwersji tam i z powrotem: {actual}"

