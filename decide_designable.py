from igraph import Graph
from itertools import product

from convert_representation import convert_parenthesized_to_tree

# ================================================================================
# 2. Funkcja (moduł) oceniająca projektowalność

import sys

import numpy as np

min_loop_length = 0

def pair_check(tup):
    if tup in [('A', 'U'), ('U', 'A'), ('C', 'G'), ('G', 'C')]:
        return True
    return False

def add_tuples(tuple1, tuple2):
    # Check if the input tuples have the same length
    if len(tuple1) != len(tuple2):
        raise ValueError("Input tuples must have the same length")

    # Use a list comprehension to add corresponding elements
    result_tuple = tuple(t1 + t2 for t1, t2 in zip(tuple1, tuple2))
    return result_tuple

memo = {}
def OPT_COUNT(i,j,sequence) -> (int, int):
    if (i, j) in memo:
        return memo[(i, j)]
    if i >= j:
        return (0, 1)

    unpaired = OPT_COUNT(i, j-1, sequence) # (max,ilosc)
    pairing = [add_tuples(add_tuples((1, 0), OPT_COUNT(i, t - 1, sequence)), OPT_COUNT(t + 1, j - 1, sequence)) for t in range(i, j) \
               if pair_check((sequence[t], sequence[j]))]
    if not pairing:
        pairing = [(0,0)]

    pairing.append(unpaired)
    max_value = max(pairing, key=lambda x: x[0])[0]
    count = sum(item[1] for item in pairing if item[0] == max_value)
    result = (max_value, count)
    memo[(i,j)] = result
    return result

#initialize matrix with zeros where can't have pairings
def initialize(N):
    #NxN matrix that stores the scores of the optimal pairings.
    DP = np.empty((N,N),dtype=object)
    DP[:] = np.NAN
    for k in range(0, min_loop_length):
        for i in range(N-k):
            j = i + k
            DP[i][j] = (0, 0)
    return DP

def nussinov(sequence,level:int):
    N = len(sequence)
    DP = initialize(N)
    structure = []

    #fill the DP matrix diagonally
    for k in range(min_loop_length, N):
        for i in range(N-k):
            j = i + k
            DP[i][j] = OPT_COUNT(i,j, sequence)

    if DP[0,N-1][1] == DP[0,N - 1][0] + 1 and DP[0,N-1][0] == level:
        return True

    return False

def generate_sequence(g: Graph, v: int) -> list[str]:
    pairs = [("A", "U"), ("U", "A"), ("C", "G"), ("G", "C")]
    letters = ['C', 'G', 'A', 'U']
    outputs = []
    if g.neighborhood_size(v, 1, "out") == 1:
        # children dots
        for i in {0, 2}:
            for letter in letters[i:i+2]:
                output = letter * g.vs[v]["unpaired_count_0"]
                for pair in pairs[i:i+2]:
                    outputs.append(pair[0] + output + pair[1])
        outputs = add_dots(g, v, outputs)
        return outputs

    prev_outputs = [""]

    for u in g.neighbors(v, "out"):
        prev_outputs = [''.join(pair) for pair in product(prev_outputs, generate_sequence(g, u))]


    if g.vs[v]["is_root"] == True:
        for output in prev_outputs:
            if output.count('.') > 0:
                for letter in letters:
                    outputs.append(output.replace('.', letter))
            else:
                outputs.append(output)
        return outputs
    for p in pairs:
        for output in prev_outputs:
            if output.count('.') > 0:
                for letter in letters:
                    if letter != p[0] and letter != p[1]:
                        outputs.append(p[0] + output.replace('.', letter) + p[1])
            else:
                outputs.append(p[0] + output + p[1])

    outputs = add_dots(g, v, outputs)
    return outputs


def add_dots(g: Graph, v: int, prev_outputs: list[str]) -> list[str]:
    # jeśli jesteśmy w rootcie (nie mamy rodzica) 
    # to nie dodajemy żadnych kropek
    if g.vs[v]["is_root"]:
        return prev_outputs 
    else:
        # indeks rodzica
        parent = g.predecessors(v)[0] 
        # którym od lewej dzieckiem rodzica jesteśmy? 
        # (równoważnie: ile dzieci naszego rodzica ma niższy indeks od nas)
        index = sum(n < v for n in g.neighbors(parent, mode='out')) 
        # każde dziecko dodaje kropki po swojej prawej stronie (jeśli jakieś są)
        right_dots_count = g.vs[parent].attributes().get(f"unpaired_count_{index + 1}") or 0 
        # pierwsze dziecko od lewej dodaje także krokpki po swojej lewej stronie
        left_dots_count = g.vs[parent]["unpaired_count_0"] if index == 0 else 0 
        return [('.' * left_dots_count + po + '.' * right_dots_count) for po in prev_outputs]

def check_symmetric(a, tol=1e-8):
    return np.all(np.abs(a-a.T) < tol)


def insert_string_at_indexes(main_string, insert_string, indexes) -> str:
    result_list = list(main_string)

    for index, char in zip(indexes, insert_string):
        result_list.insert(index, char)

    result_string = ''.join(result_list)
    return result_string


def check_designable(structure: str, rna_sequences: list[str], dot_indexes: list[int], st_level: int) -> (bool, str):
    # we create possible sequences by adding letters on dot_indexes
    letters = ['A', 'U', 'C', 'G']
    #combinations = list(product(letters, repeat=dot_indexes.__len__()))

    for sequence in rna_sequences:
        # for combination in combinations:
        memo.clear()
            # whole_sequence = insert_string_at_indexes(sequence, combination, dot_indexes)
        # teraz chcemy sprawdzic czy dla tego ciagu rna istenieje tylko jedna struktura optymalna
        if nussinov(sequence, st_level):
            return True, sequence

    return False, ""


def decide_designable(St: str) -> (bool, str):
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
    st_level = St.count('(')
    g = convert_parenthesized_to_tree(St)
    rna_sequences = generate_sequence(g, 0)
    #print(rna_sequences)
    return check_designable(St, rna_sequences, dot_indexes, st_level)
