import sys
from main import main
from typing import Iterator, Tuple

def batch_compare_designability(file_path: str) -> Iterator[Tuple[str, str, bool, bool]]:
    """
    Compare results of main.py for two structures in each line of file_path,
    returns all mismatches.
    return: Iterator of tuples (structure1, structure2, result1, result2)
        structure1, structure2 - structures from file_path
        result1, result2 - is structure 1 and 2 designable
    """
    with open(file_path, 'r') as file:
        for line in file:
            structure1, structure2 = line.strip().split()

            result1 = main(0, structure1, verbose=False)
            result2 = main(0, structure2, verbose=False)

            if result1 != result2:
                yield structure1, structure2, result1, result2

if __name__ == "__main__":
    # zweryfikuj poprawnośc argumentów
    if len(sys.argv) != 2:
        print("Usage: python3 compare_designability.py <file_path>")
        sys.exit(1)
    for structure1, structure2, result1, result2 in batch_compare_designability(sys.argv[1]):
        print("================")
        print("MISMATCH")
        print()
        print(structure1)
        main(0, structure1, verbose=True)
        print()
        print(structure2)
        main(0, structure2, verbose=True)
        print("================")