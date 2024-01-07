import sys

from igraph import Graph

from convert_representation import convert_parenthesized_to_tree
from decide_designable import decide_designable
from show_drawing import show_drawing
from utils import is_structure_with_known_ND_motifs

RESULTS_CACHE_PATH = "./results_cache.txt"
results_cache_enabled_arg = True

# ================================================================================
# 4. UI/obsługa plus spięcie tego w całość
# Na razie UI jest takie, że uruchamiamy program z dwoma argumentami:
# python3 prog.py m "((.(..(..).....))).."
# Po szczegóły zobacz funkcję "usage()" poniżej.
# - drugi parametr to reprezentacja nawiasowa struktury RNA, podana jako łańcuch znaków (str).
# Użycie:
#   python3 prog.py 2 "((.(..(..).....))).."
#   Tutaj '2' to tryb działania programu, a "((.(..(..).....))).." to struktura RNA do analizy.

def main(mode: int, structure: str):
    """
    Główna funkcja obsługująca logikę programu.
    
    Args:
        mode (int): Tryb działania programu (szczegóły: zobacz funkcję usage() poniżej), gdzie:
                    0 = tylko ocena projektowalności,
                    1 = tylko wyświetlenie struktury,
                    2 = wyświetlenie i ocena projektowalności,
                    3 = ocena i wyświetlenie jeśli projektowalna,
                    4 = ocena i wyświetlenie jeśli nieprojektowalna.
        structure (str): Reprezentacja nawiasowa struktury RNA.
    Raises:
        Exception: TODO
    """

    try:
        g = convert_parenthesized_to_tree(structure)
    except ValueError as e:
        print("WRONG STRUCTURE")
        print(str(e))
        sys.exit(1)
    
    if mode == 0:
        __mode_0(g)
    elif mode == 1:
        __mode_1(g)
    elif mode == 2:
        __mode_2(g)
    elif mode == 3:
        __mode_3(g)
    elif mode == 4:
        __mode_4(g)

def __mode_0(g: Graph) -> bool:
    """
    0 = Decide if the structure is designable. 
    Will print exactly one or exactly two lines. 
    First line: 'D' for designable, 'ND' for not designable, 
    'WRONG STRUCTURE' if the structure is incorrect. 
    Second line: details if available.
    """
    if results_cache_enabled_arg:
        result = read_result_from_file(structure)
        if result is not None:
            if result[0]:
                print("D")
                print(result[1])
            else:
                print("ND")
            return result

    contains_ND_motifs, which_motif = is_structure_with_known_ND_motifs(g)
    if contains_ND_motifs:
        print("ND")
        print(which_motif)
        return False

    designable, rna_str = decide_designable(structure)
    if designable:
        print("D")
        save_result_to_file(True, structure, rna_str)
        print(rna_str)
        return True
    else:
        print("ND")
        save_result_to_file(False, structure, "")
        return False

def __mode_1(g: Graph) -> None:
    """
    1 = Display the RNA structure as a graph
    """
    show_drawing(g, draw_unpaired=False, Sp=structure)

def __mode_2(g: Graph) -> None:
    """
    2 = Display the RNA structure and decide if it is designable
    """
    __mode_1(g)
    __mode_0(g)

def __mode_3(g: Graph) -> None:
    """
    3 = Check if the RNA structure is designable and display it if it is
    """
    if __mode_0(g):
        __mode_1(g)


def __mode_4(g: Graph) -> None:
    """
    4 = Check if the RNA structure is designable and display it if it is not
    """
    if not __mode_0(g):
        __mode_1(g)

def save_result_to_file(result: bool, structure: str, rna_str: str) -> None:
    """
    Zapisuje wynik analizy struktury RNA do pliku.
    
    Args:
        result (bool): True jeśli struktura jest projektowalna, False jeśli nie.
        structure (str): Reprezentacja nawiasowa struktury RNA.
        rna_str (str): Znalezione RNA foldujące się optymalnie do struktury (jeżeli struktura ND, to ten parametr powinien mieć wartość "").
    """
    with open(RESULTS_CACHE_PATH, "a") as f:
        f.write(f"{structure} {result} {rna_str}\n")

def read_result_from_file(structure: str) -> (bool, str):
    """
    Odczytuje wynik analizy struktury RNA z pliku. 
    Jeśli brak jest pliku lub brak jest wyniku dla danej struktury, zwraca None.
    
    Args:
        structure (str): Reprezentacja nawiasowa struktury RNA.
    Returns:
        bool: True jeśli struktura jest projektowalna, False jeśli nie.
        str: Znalezione RNA foldujące się optymalnie do struktury (jeżeli struktura ND, to ten parametr ma wartość "").
    """
    try:
        with open(RESULTS_CACHE_PATH, "r") as f:
            for line in f:
                if line.startswith(structure+" "):
                    if line.split(" ")[1].strip() == "True":
                        return (True, line.split(" ")[2].strip())
                    else:
                        print("deb " +line.split(" ")[1].strip())
                        return (False, "")
    except FileNotFoundError:
        return None

    return None

def usage():
    print("Usage: python3 main.py <mode> '<structure>' <results_cache_enabled>")
    print("       <mode> should be an integer between 0 and 4, where:")
    print("       0 = Decide if the structure is designable. Will print exactly one or exactly two lines. First line: 'D' for designable, 'ND' for not designable, 'WRONG STRUCTURE' if the structure is incorrect. Second line: details if available.")
    print("       1 = Display the RNA structure as a graph")
    print("       2 = Display the RNA structure and decide if it is designable")
    print("       3 = Check if the RNA structure is designable and display it if it is")
    print("       4 = Check if the RNA structure is designable and display it if it is not")
    print("       <structure> is the parenthesized representation of the RNA structure to analyze.")
    print("       <results_cache_enabled> is an int value indicating whether to use the results cache file (default: 1). If 0, the program will not use the results cache file. The cache file is at " + RESULTS_CACHE_PATH + ".")
    sys.exit(1)

if __name__ == "__main__":
    if not 3 <= len(sys.argv) <= 4:
        usage()
    mode = int(sys.argv[1])
    if mode < 0 or mode > 4:
        print("Mode must be an integer between 0 and 4.\n")
        usage()
    structure = sys.argv[2]
    if any(char not in ".()" for char in structure):
        print("Structure must be a string containing only '.' and '(', ')'.\n")
        usage()
    if len(sys.argv) == 4:
        results_cache_enabled_arg = sys.argv[3] != "0"

    main(mode, structure)