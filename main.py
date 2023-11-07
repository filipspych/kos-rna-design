import sys

# ================================================================================
# 4. UI/obsługa plus spięcie tego w całość
# Na razie UI jest takie, że uruchamiamy program z dwoma argumentami:
# python3 prog.py m "((.(..(..).....))).."
# gdzie:
# - pierwszy parametr (m) to tryb działania programu, reprezentowany przez liczbę całkowitą:
#   0 - zdecyduj, czy struktura jest projektowalna. Wypisz 'D' jeśli projektowalna, 'ND' jeśli nieprojektowalna lub 'ZLA STRUKTURA', jeśli struktura nawiasowa jest niepoprawna.
#   1 - wyświetl strukturę RNA jako graf.
#   2 - wyświetl strukturę RNA i ocen, czy jest projektowalna.
#   3 - sprawdź, czy struktura RNA jest projektowalna, i wyświetl ją, jeśli jest projektowalna.
#   4 - sprawdź, czy struktura RNA jest projektowalna, i wyświetl ją, jeśli nie jest projektowalna.
# - drugi parametr to reprezentacja nawiasowa struktury RNA, podana jako łańcuch znaków (str).
# Użycie:
#   python3 prog.py 2 "((.(..(..).....))).."
#   Tutaj '2' to tryb działania programu, a "((.(..(..).....))).." to struktura RNA do analizy.

def main(mode: int, structure: str):
    """
    Główna funkcja obsługująca logikę programu.
    
    Args:
        mode (int): Tryb działania programu, gdzie:
                    0 = tylko ocena projektowalności,
                    1 = tylko wyświetlenie struktury,
                    2 = wyświetlenie i ocena projektowalności,
                    3 = ocena i wyświetlenie jeśli projektowalna,
                    4 = ocena i wyświetlenie jeśli nieprojektowalna.
        structure (str): Reprezentacja nawiasowa struktury RNA.
    Raises:
        Exception: TODO
    """
    # TODO: Implementacja logiki w zależności od trybu
    pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 prog.py <mode> '<structure>'")
        print("       <mode> should be an integer between 0 and 4, where:")
        print("       0 = Decide if the structure is designable ('D' for designable, 'ND' for not designable, 'WRONG STRUCTURE' if the structure is incorrect)")
        print("       1 = Display the RNA structure as a graph")
        print("       2 = Display the RNA structure and decide if it is designable")
        print("       3 = Check if the RNA structure is designable and display it if it is")
        print("       4 = Check if the RNA structure is designable and display it if it is not")
        print("       <structure> is the parenthesized representation of the RNA structure to analyze.")
        sys.exit(1)

    mode = int(sys.argv[1])
    structure = sys.argv[2]

    main(mode, structure)