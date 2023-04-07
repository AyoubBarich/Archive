from automata import Automata


Sigma = {'a', 'b'}
states = {0, 1, 2}
trans = {
    0: {'a': {1}},
    1: {'b': {1, 2}, 'a': {1}}
}
ini = {0}
final = {2}
A = Automata(Sigma, states, trans, ini, final)

ini = {0, 1}
B = Automata(Sigma, states, trans, ini, final)

trans = {
    0: {'a': {1}},
    1: {'b': {2}, 'a': {1}}
}
ini = {0}

C = Automata(Sigma, states, trans, ini, final)

trans = {
    0: {'a': {1}, 'b':{2}},
    1: {'b': {2}, 'a': {1}},
    2: {'a': {1,2}, 'b':{0}}
}

D = Automata(Sigma, states, trans, ini, final)


def test_isdeterministic():
    # A a deux transitions à partir de 1 sur b
    assert(A.is_deterministic(True) == False)
    # B a deux états initiaux
    assert(B.is_deterministic(False) == False)
    # C est déterministe
    assert(C.is_deterministic(False) == True)

def test_iscomplete():
    assert(A.is_complete() == False)
    assert(D.is_complete() == True)
    

def test_compute_next():
    X = {1,2}
    letter = 'a'
    Y = {1}
    assert(A.compute_next(X,letter) == Y)
    letter = 'b'
    assert(A.compute_next(X,letter) == X)
    return

def test_accept():
    assert(A.accept('ab')== True)
    assert(B.accept('b')== True)
    return


# def test_intersection():
#     """Should compute the intersection between two DFAs"""
#     # This DFA accepts all words which contain at least four
#     # occurrences of 1
#     dfa1 = Automata(
#         {'a', 'b'},
#         {0, 1, 2, 3, 4},
        
#         {
#             0: {'a': {0}, 'b': {1}},
#             1: {'a': {1}, 'b': {2}},
#             2: {'a': {2}, 'b': {3}},
#             3: {'a': {3}, 'b': {4}},
#             4: {'a': {4}, 'b': {4}}
#         },
#         {0},
#         {4}
#     )
#     # This DFA accepts all words which do not contain two
#     # consecutive occurrences of 1
#     dfa2 = Automata(
#         {'a', 'b'},
#         {0, 1, 2},
#         {
#             0: {'a': {0}, 'b': {1}},
#             1: {'a': {0}, 'b': {2}},
#             2: {'a': {2}, 'b': {2}}
#         },
#         {0},
#         {0, 1}
#     )
#     new_dfa = dfa1.intersection(dfa2)
#     assert(new_dfa.states == {
#         (0, 0),
#         (1, 0), (1, 1),
#         (2, 0), (2, 1), (2, 2),
#         (3, 0), (3, 1), (3, 2),
#         (4, 0), (4, 1), (4, 2)
#     })
#     assert(new_dfa.alphabet=={'a', 'b'})
#     assert(new_dfa.trans=={
#         (0, 0): {'a': {(0, 0)}, 'b': {(1, 1)}},
#         (1, 0): {'a': {(1, 0)}, 'b': {(2, 1)}},
#         (1, 1): {'a': {(1, 0)}, 'b': {(2, 2)}},
#         (2, 0): {'a': {(2, 0)}, 'b': {(3, 1)}},
#         (2, 1): {'a': {(2, 0)}, 'b': {(3, 2)}},
#         (2,2): {'a': {(2, 20)}, 'b': {(3, 2)}},
#         (3, 0): {'a': {(3, 0)}, 'b': {(4, 1)}},
#         (3, 1): {'a': {(3, 0)}, 'b': {(4, 2)}},
#         (3,2): {'a': {(3, 2)}, 'b': {(4, 2)}},
#         (4, 0): {'a': {(4, 0)}, 'b': {(4, 1)}},
#         (4, 1): {'a': {(4, 0)}, 'b': {(4, 2)}},
#         (4,2): {'a': {(4,2)}, 'b': {(4, 2)}}
#     })
#     assert(new_dfa.ini==(0, 0))
#     assert(new_dfa.final== {
#         (4, 0), (4, 1),
#     })

#     # Test retain names logic without minify
#     assert(dfa1.intersection(dfa2) == new_dfa)

def test_determinize():
    
    # B4: (a+b)^*.b  (non-deterministic)
    Sigma = {'a', 'b'}
    states_4 = {0, 1}
    ini_4 = {0}
    final_4 = {1}
    trans_4 = {
        0: {'a': {0}, 'b': {0,1}},
        1: {}
    }
    B4 = Automata(Sigma, states_4, trans_4, ini_4, final_4)
    assert (B4.determinize().is_deterministic()==True)