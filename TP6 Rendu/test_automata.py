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


def test_intersection():
    """Should compute the intersection between two DFAs"""
    # This DFA accepts all words which contain at least four
    # occurrences of 1
    dfa1 = Automata(
        {'0', '1'},
        {'q0', 'q1', 'q2', 'q3', 'q4'},
        
        {
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q1', '1': 'q2'},
            'q2': {'0': 'q2', '1': 'q3'},
            'q3': {'0': 'q3', '1': 'q4'},
            'q4': {'0': 'q4', '1': 'q4'}
        },
        {'q0'},
        {'q4'}
    )
    # This DFA accepts all words which do not contain two
    # consecutive occurrences of 1
    dfa2 = Automata(
        {'0', '1'},
        {'p0', 'p1', 'p2'},
        {
            'p0': {'0': 'p0', '1': 'p1'},
            'p1': {'0': 'p0', '1': 'p2'},
            'p2': {'0': 'p2', '1': 'p2'}
        },
        {'p0'},
        {'p0', 'p1'}
    )
    new_dfa = dfa1.intersection(dfa2)
    assert(new_dfa.states == {
        ('q0', 'p0'),
        ('q1', 'p0'), ('q1', 'p1'),
        ('q2', 'p0'), ('q2', 'p1'), ('q2', 'p2'),
        ('q3', 'p0'), ('q3', 'p1'), ('q3', 'p2'),
        ('q4', 'p0'), ('q4', 'p1'), ('q4', 'p2')
    })
    assert(new_dfa.alphabet=={'0', '1'})
    assert(new_dfa.trans=={
        ('q0', 'p0'): {'0': ('q0', 'p0'), '1': ('q1', 'p1')},
        ('q1', 'p0'): {'0': ('q1', 'p0'), '1': ('q2', 'p1')},
        ('q1', 'p1'): {'0': ('q1', 'p0'), '1': ('q2', 'p2')},
        ('q2', 'p0'): {'0': ('q2', 'p0'), '1': ('q3', 'p1')},
        ('q2', 'p1'): {'0': ('q2', 'p0'), '1': ('q3', 'p2')},
        ('q2', 'p2'): {'0': ('q2', 'p2'), '1': ('q3', 'p2')},
        ('q3', 'p0'): {'0': ('q3', 'p0'), '1': ('q4', 'p1')},
        ('q3', 'p1'): {'0': ('q3', 'p0'), '1': ('q4', 'p2')},
        ('q3', 'p2'): {'0': ('q3', 'p2'), '1': ('q4', 'p2')},
        ('q4', 'p0'): {'0': ('q4', 'p0'), '1': ('q4', 'p1')},
        ('q4', 'p1'): {'0': ('q4', 'p0'), '1': ('q4', 'p2')},
        ('q4', 'p2'): {'0': ('q4', 'p2'), '1': ('q4', 'p2')}
    })
    assert(new_dfa.ini==('q0', 'p0'))
    assert(new_dfa.final== {
        ('q4', 'p0'), ('q4', 'p1'),
    })

    # Test retain names logic without minify
    assert(dfa1.intersection(dfa2) == new_dfa)
