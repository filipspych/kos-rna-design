from igraph import Graph

from convert_representation import convert_parenthesized_to_tree

# ================================================================================
# 2. Funkcja (moduł) oceniająca projektowalność


def generate_sequence(g: Graph, v: int) -> list[str]:

    if g.neighborhood_size(v, 1, "out") == 1:
        return ["AU", "UA", "CG", "GC"]

    outputs = []
    prev_outputs = [""]

    pairs = [("A", "U"), ("U", "A"), ("C", "G"), ("G", "C")]
    new_prev_outputs = []
    for u in g.neighbors(v, "out"):
        node_outputs = generate_sequence(g, u)
        print(node_outputs)
        for prev_output in prev_outputs:
            for new_output in node_outputs:
                new_prev_outputs.append(prev_output + new_output)

        prev_outputs = new_prev_outputs

        new_prev_outputs = []
    if v == 0:
        return prev_outputs
    for p in pairs:
        for output in prev_outputs:
            outputs.append(p[0] + output + p[1])

    return outputs
def generate_rna_sequences(parentheses_string):
    def backtrack(current_sequence, remaining_pairs):
        if not remaining_pairs:
            result.append(current_sequence)
            return

        for pair in remaining_pairs:
            open_bracket, close_bracket = pair
            if open_bracket in current_sequence and current_sequence.count(open_bracket) > current_sequence.count(close_bracket):
                continue

            new_sequence = current_sequence + open_bracket + close_bracket
            new_pairs = remaining_pairs.copy()
            new_pairs.remove(pair)
            backtrack(new_sequence, new_pairs)

    result = []
    pairs = [("A", "U"), ("U", "A"), ("C", "G"), ("G", "C")]
    backtrack("", pairs)

    return result


def decide_designable(St: str) -> bool:
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
    #raise Exception("Nie zaimplementowano.")
    # find . indexes
    dot_indexes = [i for i, char in enumerate(St) if char == '.']

    g = convert_parenthesized_to_tree(St)

    output = generate_sequence(g,0)
    print(output)