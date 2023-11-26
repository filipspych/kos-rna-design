import shlex
import tempfile
import matplotlib.pyplot as plt
import igraph
from sys import platform
from igraph import Graph, os

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
    # TODO: treść funkcji
    plot_graph(St, draw_unpaired)


def plot_graph(g: Graph, draw_unpaired: bool):
    windows: bool = True if platform == "win32" else False
    filename = tempfile.NamedTemporaryFile(suffix=".pdf").name
    show_svg(g, filename, windows)


def show_svg(g: Graph, filename: str, windows):
    color_dict = {False: "blue", True: "red"}
    layout = g.layout_reingold_tilford(root=[0])
    g.vs["color"] = [color_dict[isPaired] for isPaired in g.vs["isPaired"]]

    igraph.plot(g, layout=layout, target=filename)

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