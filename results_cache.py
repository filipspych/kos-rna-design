RESULTS_CACHE_PATH = "./results_cache.txt"

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
                        return (False, "")
    except FileNotFoundError:
        return None

    return None
