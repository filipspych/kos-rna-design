# Narzędzie do Projektowania Struktury RNA
Pamiętajcie żeby najpierw zainstalować igraph. u mnie: `pip3 install python-igraph`

Nasz zespołowy GitHub: [https://github.com/filipspych/kos-rna-design/tree/develop](https://github.com/filipspych/kos-rna-design/tree/develop) (zaproszenia na mailu). Poniżej proponowany podział pracy.

**UWAGA**: Repozytorium GitHub jest publiczne (ale prawa edycji mają tylko contributorzy).

## Jak pracujemy

Pracujemy na gałęzi `develop`, gałąź `main` zostawiamy na ostateczny wynik pracy.
**BŁAGAM, WE WSPÓLNYM KODZIE (NA STYKU MODUŁÓW) UŻYWAJMY PYTHONOWYCH TYPÓW.**
W Pythonie oficjalnie (zgodnie z PEP) indentacja spacjami (wiem...).

## Co robimy

Ogólnie, chcemy zrobić narzędzie, które wesprze nasze teoretyczne rozważania. Pierwsza wersja programu pozwoli nam automatycznie (w sensie nie licząc tego ręcznie) sprawdzić czy dane S jest projektowalne czy nie. W tym celu potrzebujemy następujących komponentów:

1. **Obiekt drzewa struktury**: główny obiekt do przekazywania między strukturami. To będzie obiekt z biblioteki igraph. @Filip Spychała

2. **Funkcja (moduł) oceniająca projektowalność**: @Borys Kurdek Linki do prac opisujących algorytmy zostały podane w pracy 1, strona 2. Można również użyć czegoś stąd:
   - seqfold · PyPI: [https://pypi.org/project/seqfold/](https://pypi.org/project/seqfold/)
   - TBI - ViennaRNA Package 2, zwłaszcza metoda Wuchty et.al 1999: [https://www.tbi.univie.ac.at/RNA/](https://www.tbi.univie.ac.at/RNA/)
   - ViennaRNA Web Services: [http://rna.tbi.univie.ac.at/](http://rna.tbi.univie.ac.at/)

3. **Funkcja (moduł) wyświetlający drzewo na ekranie**: @Michal Oledzki, polecam wzorować się na tym (gotowe rozwiązanie): [https://github.com/filipspych/pace-challange-BDS/blob/feature/PS_analysis/plot.py](https://github.com/filipspych/pace-challange-BDS/blob/feature/PS_analysis/plot.py)

4. **Funkcja (moduł) zamieniająca reprezentację nawiasową w drzewo i vice versa**: @Filip Spychała

5. **"UI"/obsługa + spięcie tego w całość**: @Filip Spychała

Stworzyłem osobne pliki na te moduły w repozytorium. Jeżeli ktośkolwiek ma jakieś propozycje, to oczywiście śmiało wprowadzać w życie/mówić.

## Sygnatury

Tutaj definicje funkcji, żeby to wszystko mogło ze sobą działać.

```python
from igraph import Graph
from typing import NoReturn
import sys

# ================================================================================
# 1. drzewo struktury. 
#struktura bedzie dana jako graph w igraph. szczegoly dot samej bilbioteki igraph sa w sekcji nizej.
# w grafie przechowujemy tylko wierzcholki sparowane (nawiasy) natomiast wierzcholki niesparowane sa reprezentowane przez liczby (poniewaz sa one nierozroznialne). liczby sa dane jako parametry tego wierzcholka.
# v["unpaired_count_0"]
# v["unpaired_count_1"]
# dodatkowo w roocie mamy v["is_root"] = True, wszedzie indziej ofc = False. w rootcie mamy też v["unpaired_count_2"], poniewaz root moze miec 2 sparowane dzieci i dodatkowo dowolną liczbę niesparowanych dzieci (pozostale wierzcholki jak maja 2 sparowanych dzieci to nie moga juz miec zadnych niesparowanych, bo wpp sa nieprojektowalne)
# dlaczego parametry sa tylko 3? dlatego ze plan jest taki zeby to drzewo moglo przechowywac tylko grafy nie zawierajace m3o ani m5. zatem: ROOT MOZE MIEC 4, 3, 2, 1 lub 0 sparowanych dzieci ( czyli "()" a nie "."). JEZELI MA 4 lub 3 sparowane dzieci TO MA DOIKLADNIE 0 NIESPAROWANYCH DZIECI (wpp moze miec dowolną liczbę niesparowanych). NIE-ROOT moze miec 3, 2, 1, lub 0 sparowanych dzieci i jesli ma 3 lub 2 niesparowane dzieci, to musi miec dokladnie 0 niesprowanych dzieci (wpp moze miec dowolna liczbe niesparowanych).
# CO Z KOLEJNOSCIA?: za kolejnosc dzieci w nodzie ustalmy kolejnosc ich indeksow (vertex ID)

# ================================================================================
# 2. Funkcja (moduł) oceniająca projektowalność
def decide_designable(St: Graph) -> bool:
    """
    Ocenić, czy struktura RNA reprezentowana przez graf St jest projektowalna. TODO: tutaj dodac dodatkowe info, ktore moze byc przydatne dla uzytkownikow tej funkcji
    
    Args:
        St (Graph): Struktura RNA reprezentowana jako graf w igraph.
        
    Raises:
        Exception: TODO Wyjątek rzucany, gdy nie można podać odpowiedzi. Czy to sie moze zdarzy? Jezeli nie to zmodyfikowac dokum,entacje.
        
    Returns:
        bool: True jeśli St jest projektowalna, False jeśli nie jest projektowalna.
    """
    # TODO: treść funkcji
    raise Exception("Komunikat o błędzie. Im bardziej szczegółowy, tym lepiej")

# ================================================================================
# 3. Funkcja (moduł) wyświetlający drzewo na ekranie
def show_drawing(St: Graph, draw_unpaired: bool = True, Sp: str = "") -> NoReturn:
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
    raise Exception("Komunikat o błędzie. Im bardziej szczegółowy, tym lepiej")

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
    pass

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
```

## Przykłady użycia igraph

Aby rozpocząć, zainstaluj igraph używając polecenia:
```pip install python-igraph```

Dokumentacja dla Pythona jest dostępna pod adresem: [igraph Python API](https://igraph.org/python/api/latest/igraph._igraph.GraphBase.html).

### Prosty przykład:

```python
from igraph import Graph

g = Graph()
g.add_vertices(3)
g.add_edges([(0, 1), (1, 2)])
print(g)
```

Kolejność wierzchołków w węźle w igraph jest taka, jak kolejność ich vertex ID, a kolejność vertex ID jest taka, jak kolejność ich dodawania. Istnieje możliwość permutacji wierzchołków (permute.vertices), jednak jest to funkcjonalność z pakietu R igraph, pytanie czy w Pythonie też jest dostępne. Jeżeli nie, to trzeba robić to ręcznie (tworząc nowy graf dodając wierzchołki w innej kolejności).

Do atrybutów wierzchołków można się dostać w ten sposób:

```for v in g.vs:
    v["unpaired_count_1"] = 0  # Tutaj przykładowa wartość
    v["unpaired_count_2"] = 0  # Tutaj przykładowa wartość
    if v["is_root"]:
        v["unpaired_count_3"] = 0  # Tutaj przykładowa wartość

v["is_root"] = False
```
Sąsiedzi:
```g.neighbors(vertexID)```

# Zwraca sąsiadujące wierzchołki danego wierzchołka.
Igraph ma mnóstwo skróconych zapisów, ale trzeba uważać. Nie wszystkie są tak samo optymalne! Na przykład wygląda na to, że g.vs przywołuje z pamięci wszystkie wierzchołki w sposób eager, a nie lazy, co oznacza, że filtrowanie ich potem po indeksie działa bardzo wolno (szybciej wyszukać bezpośrednio z grafu g).

Kolejne kroki

W kolejnych wersjach następujące rozszerzenia programu (kolejność na liście bez znaczenia):

Zdefiniujmy: Mówimy, że struktura S jest minimalnie nieprojektowalna (S \in MND) wtedy i tylko wtedy, gdy S \in ND i dla każdego liścia x, mamy S\x \in D.
 - [ ] Czy zamiana kolejności poddrzew może zmienić klasę ND/D struktury? Napisać program, który będzie szukał kontrprzykładów.
 - [ ] Przeszukiwacz przestrzeni MND (losowo/po kolei szukamy S \in MND).
