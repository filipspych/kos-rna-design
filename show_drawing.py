import shlex
import tempfile
import matplotlib.pyplot as plt
import igraph
from sys import platform
from igraph import Graph, os

from convert_representation import convert_parenthesized_to_naive_tree, convert_subtree_to_parenthesized, convert_tree_to_parenthesized
from convert_representation import convert_parenthesized_to_numberized

# ================================================================================
# 3. Funkcja (moduł) wyświetlający drzewo na ekranie
def show_drawing(St: Graph, draw_unpaired: bool = True, Sp: str = "") -> None:
    """
    Wyświetla drzewo struktury RNA na ekranie.  TODO: tutaj dodac dodatkowe info, ktore moze byc przydatne dla uzytkownikow tej funkcji
    
    Args:
        St (Graph): Struktura RNA reprezentowana jako graf (S tree).
        draw_unpaired (bool, optional): Jeśli True, niesparowane wierzchołki będą rysowane. Domyślnie True.
        Sp (str): Reprezentacja nawiasowa struktury RNA (S parenthesized).
    
    Raises:
        Exception: Wyjątek rzucany, gdy nie można wyświetlić rysunku. TODO: Czy to sie moze zdarzy? Jezeli nie to zmodyfikowac dokum,entacje.
    """
    plot_graph(St, draw_unpaired, convert_parenthesized_to_numberized(Sp))

def __convert_to_drawable_graph(g: Graph, draw_unpaired: bool, rootLabelSuffix: str) -> Graph:
    """
    Konwertuje graf reprezentujący strukturę RNA na graf, który można narysować.
    
    Args:
        g (Graph): Graf reprezentujący strukturę RNA.
    
    Returns:
        Graph: Graf, który można narysować.
    """
    if draw_unpaired:
        drawable_graph = convert_parenthesized_to_naive_tree(convert_tree_to_parenthesized(g))
        drawable_graph.vs["label"] = [str(i) for i in range(drawable_graph.vcount())]
    else:
        drawable_graph = g
        for v in drawable_graph.vs:
            v["isPaired"] = True
            if v["is_root"]:
                v["label"] = rootLabelSuffix
            else:
                v["label"] = convert_parenthesized_to_numberized(convert_subtree_to_parenthesized(g, v.index))
    return drawable_graph

def plot_graph(g: Graph, draw_unpaired: bool, rootLabelSuffix: str) -> None:
    windows: bool = True if platform == "win32" else False
    filename = tempfile.NamedTemporaryFile(suffix=".pdf").name
    __show_svg(__convert_to_drawable_graph(g, draw_unpaired, rootLabelSuffix), filename, windows)


def __show_svg(g: Graph, filename: str, windows):
    color_dict = {False: "white", True: "red"}
    layout = g.layout_reingold_tilford(root=[0])
    g.vs["color"] = [color_dict[isPaired] for isPaired in g.vs["isPaired"]]

    igraph.plot(g, layout=layout, target=filename, vertex_label=g.vs["label"])

    # EDGE_THICKNESS: float = 0.3
    # VERTEX_SIZE: int = 5
    # LAYOUT: str = "rt"
    # WIDTH = 100
    # HEIGHT = 100
    # g.write_svg(
    #     fname=filename,
    #     vertex_size=VERTEX_SIZE,
    #     edge_stroke_widths=[EDGE_THICKNESS] * g.ecount(),
    #     font_size=VERTEX_SIZE,
    #     width=WIDTH,
    #     height=HEIGHT,
    #     layout=g.layout(LAYOUT, [0]),
    #     colors=[color_dict[isPaired] for isPaired in g.vs["isPaired"]]
    # )

    if windows:
        os.system("start " + filename)  # windows
    else:
        os.system("open " + shlex.quote(filename))  # MacOS/X