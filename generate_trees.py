import random
import sys

from igraph import Graph

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
def generate_tree(n: int) -> Graph:
    #chcemy wygenerowac drzewo ktorego lanuych ma dlugosc n
    stack = []
    g: Graph
    g = Graph()
    g.add_vertex()
    g.vs[0]["isPaired"] = True
    root_paired = random.randint(0,4)
    n -= root_paired
    root_unpaired = 0
    if root_paired == 0:
        g.vs[0]["unpaired_count_0"] = n
        return g
    elif root_paired == 1 or 2:
        root_unpaired = random.randint(0,n)

    n -= root_unpaired
    child_amount = root_paired + root_unpaired
    pair_indexes = random.sample(range(1, child_amount + 1), root_paired)





    raise Exception("unimplemented")

def generate_trees(amount: int, path: str):
    raise Exception("unimplemented")


#if __name__ == "__main__":
