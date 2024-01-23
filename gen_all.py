import sys

from main import main
import itertools

PROJEKTOWALNE_PATH = './PROJEKTOWALNE.txt'

# ================================================================================
# 4. UI/obsługa plus spięcie tego w całość
# Na razie UI jest takie, że uruchamiamy program z dwoma argumentami:
# python3 prog.py m "((.(..(..).....))).."
# Po szczegóły zobacz funkcję "usage()" poniżej.
# - drugi parametr to reprezentacja nawiasowa struktury RNA, podana jako łańcuch znaków (str).
# Użycie:
#   python3 prog.py 2 "((.(..(..).....))).."
#   Tutaj '2' to tryb działania programu, a "((.(..(..).....))).." to struktura RNA do analizy.

def gen_all(max_len: int):
    """
    Program generujący wszystkie projektowalne struktury rozmiaru <= max_size i zapisuje je do pliku PROJEKTOWALNE.txt
    
    Args:
        max_len(int): maksymalna długość generowanych struktur większa niż 0
    """

    with open(PROJEKTOWALNE_PATH, "a") as f:
        for i in range(max_len + 1):
            permutations = itertools.product(['(', '.', ')'], repeat=i)
            for p in permutations:
                struct = convert_tuple(p)
                result = main(0, struct, False, True)
                designable = result
                if designable:
                    f.write(f"{struct}\n")


def convert_tuple(tup):

    str = ''
    for item in tup:
        str = str + item
    return str


def usage():
    print("Usage: python3 gen_all.py <max_len>")
    sys.exit(1)

if __name__ == "__main__":
    if not 2 <= len(sys.argv) <= 2:
        usage()
    max_len = int(sys.argv[1])
    if max_len <= 0:
        print("Max length must be greater than 0.\n")
        usage()

    gen_all(max_len)