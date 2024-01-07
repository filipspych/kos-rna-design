import random
import sys

from igraph import Graph
import math
import convert_representation
from convert_representation import convert_parenthesized_to_tree

## dodatkowo w roocie mamy v["is_root"] = True, wszedzie indziej ofc = False.
# w rootcie mamy też v["unpaired_count_2"], poniewaz root moze miec 2 sparowane dzieci
# i dodatkowo dowolną liczbę niesparowanych dzieci
# (pozostale wierzcholki jak maja 2 sparowanych dzieci to nie moga juz miec zadnych niesparowanych,
# bo wpp sa nieprojektowalne)
# dlaczego parametry sa tylko 3? dlatego ze plan jest taki zeby to drzewo moglo przechowywac
# tylko grafy nie zawierajace m3o ani m5.
# zatem: ROOT MOZE MIEC 4, 3, 2, 1 lub 0 sparowanych dzieci ( czyli "()" a nie ".").
# JEZELI MA 4 lub 3 sparowane dzieci TO MA DOIKLADNIE 0 NIESPAROWANYCH DZIECI
# (wpp moze miec dowolną liczbę niesparowanych).
# NIE-ROOT moze miec 3, 2, 1, lub 0 sparowanych dzieci i jesli ma 3 lub 2 niesparowane dzieci,
# to musi miec dokladnie 0 niesprowanych dzieci (wpp moze miec dowolna liczbe niesparowanych).
# CO Z KOLEJNOSCIA?: za kolejnosc dzieci w nodzie ustalmy kolejnosc ich indeksow (vertex ID)

def process_pairs(g: Graph, pair_indexes: list[int],stack: list,paired:int, unpaired: int,parent: int) -> None:
    for pair in range(0, paired):
        current_string = "unpaired_count_" + str(pair)
        #print(current_string)
        #print(current_string)
        if paired > pair + 1:
            g.vs[parent][current_string] = pair_indexes[pair + 1] - pair_indexes[pair] - 1
            unpaired -= pair_indexes[pair + 1] - pair_indexes[pair] - 1
        else:
            g.vs[parent][current_string] = unpaired
        v = g.add_vertex()
        v["unpaired_count_0"] = 0
        g.add_edge(parent, len(g.vs) - 1)
        stack.append(v)

def generate_tree(n: int) -> Graph:
    #chcemy wygenerowac drzewo ktorego lanuych ma dlugosc n
    stack = []
    g: Graph

    g = Graph(directed=True)

    g.add_vertex()
    g.vs[0]["is_root"] = True
    root_paired = random.randint(0,min(n/2,4))
    n -= root_paired * 2
    root_unpaired = 0
    if root_paired == 0:
        g.vs[0]["unpaired_count_0"] = n
        return g
    elif root_paired == 1 or root_paired == 2:
        root_unpaired = random.randint(0,n)

    print(root_paired,root_unpaired)
    n -= root_unpaired
    print(n)
    child_amount = root_paired + root_unpaired
    pair_indexes = random.sample(range(0, child_amount), root_paired)
    pair_indexes.sort()
    print(pair_indexes)

    process_pairs(g,pair_indexes,stack,root_paired,root_unpaired,0)


    # process childs
    while len(stack) > 0:
        v = stack.pop()
        # wylicz ilosc sparowanych
        # wylicz ilosc niesparowanych
        # powtroz poprzednia opearacje
        if n <= 0:
            continue
        if n == 1:
            node_paired = 0
        else:
            node_paired = random.randint(0, min(3, math.floor(n/2)))
        node_unpaired = 0
        if node_paired == 0 or node_paired == 1:
            node_unpaired = random.randint(0, n - node_paired * 2)

        child_amount = node_paired + node_unpaired
        n -= node_paired * 2 + node_unpaired
        print(n)
        pair_indexes = random.sample(range(0, child_amount), node_paired)
        pair_indexes.sort()
        process_pairs(g,pair_indexes,stack,node_paired,node_unpaired,v.index)
        if len(stack) == 0 and n > 0:
            v["unpaired_count_0"] = n

    return g

def generate_trees(amount: int, path: str):
    raise Exception("unimplemented")


if __name__ == "__main__":
    g = generate_tree(10)
    struct = convert_representation.convert_tree_to_parenthesized(g)
    print(struct)