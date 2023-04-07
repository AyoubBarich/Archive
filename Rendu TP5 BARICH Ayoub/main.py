from automata import Automata
import test_automata as test

# Construction d'un premier automate
Sigma = {'a', 'b'}
states = {0, 1, 2,3}
trans = {
    0: {'a': {1}},
    1: {'b': {2,1}, 'a': {1}},
    2: {'a':{1},'b':{3}},
    3: {}
}
ini = {0}
final = {2,3}
# A l'aide du constructeur de la classe
A = Automata(Sigma, states, trans, ini, final)


print(A.is_empty())

"""


transB={    
    0: {'a': {0}, 'b':{0,1}},
    1: {'a': {2}},
    2: {'b': {3}},
    3: {'a': {3}, 'b':{3}}
}
B = Automata(Sigma,{0,1,2,3},transB,0,3)
print(B)
# Construction du même automate
# à l'aide des méthodes de la classe
Abis = Automata(Sigma, set(), {}, set(), set())
print(Abis)
Abis.add_state(0)
Abis.add_state(1)
Abis.add_state(2)
Abis.set_initial(0)
Abis.set_final(3)
Abis.add_transition(0, 'a', 1)
Abis.add_transition(1, 'a', 1)
Abis.add_transition(1, 'b', 1)
Abis.add_transition(1, 'b', 2)
print(Abis)
"""