"""

A class to deal with finite-state automata
P.-A. Reynier, Feb. 2023

"""

import copy


class Automata:

    def __init__(self, alphabet, states, trans, ini, final):
        """
        :param alphabet: set of symbols
        :param states: set of states
        :param trans: dictionary giving transitions
        :param ini: set of initial states
        :param final: set of final states
        """
        self.alphabet = alphabet
        self.states = states
        self.trans = trans
        self.ini = ini
        self.final = final

    def get(self,request):
        Attributes = {'self':self,
                      'alphabet':self.alphabet,
                      'states':self.states, 
                      'trans':self.trans, 
                      'ini':self.ini, 
                      'final':self.final, 
                    }
        return Attributes[request]


    def add_state(self, state):
        """
        :param state: state to be added
        :return: 1 if state successfuly added, 0 otw
        """
        if state in self.states:
            print("Error while adding state: already present")
            return 0
        try: 
            self.states.add(state)
        except:
            print("Error while adding state: set error")
            return 0
        return 1


    def add_transition(self, source, label, target): 
        """
        :param source: source state
        :param label: label of the transition
        :param target: target state
        :return: 1 if transition successfuly added, 0 otw
        """
        if source not in self.states:
            print("Error while adding transition: source state not in states")
            return 0
        if target not in self.states:
            print("Error while adding transition: target state not in states")
            return 0
        if label not in self.alphabet:
            print("Error while adding transition: label not in alphabet")
            return 0
        # source is not a key of self.trans
        if source not in self.trans:
            self.trans[source] = {}
            self.trans[source][label]={target}
        # source is a key of self.trans
        else:
            # label is not a key of self.trans[source]
            if label not in self.trans[source]:
                self.trans[source][label]={target}
            # label is a key of self.trans[source]
            else:
                self.trans[source][label].add(target)
        return 1               


    def set_initial(self,state):
        """
        :param state: a state
        :return: 1 if modification suceeded, 0 otw
        """
        if state in self.states:
            self.ini.add(state)
            return 1
        else:
            return 0


    def set_final(self,state):
        """
        :param state: a state
        :return: 1 if modification suceeded, 0 otw
        """
        if state in self.states:
            self.final.add(state)
            return 1
        else:
            return 0


    def __str__(self):
        """ Overrides print function """
        res = "Display Automaton\n"
        res += "Alphabet: " + str(self.alphabet) +"\n"
        res += "Set of states: "+str(self.states) +"\n"
        res += "Initial states "+str(self.ini) + "\n"
        res += "Final states "+str(self.final) + "\n"
        res += "Transitions:"+"\n"
        for source in self.trans:
            for label in self.trans[source]:
                for target in self.trans[source][label]:
                    res += "Transition from "+str(source)+" to "+str(target)+" labelled by "+str(label)+"\n"
        return res


    def is_deterministic(self,verbose=False):
        """
        :return: True if the automaton is deterministic, False otherwise
        """
        # Checks the number of initial states
        
        if len(self.ini) != 1:
            if verbose:
                print("Too many initial states")
            return False
        # Loop over source states
        for source in self.trans:
            # Loop over labels
            for label in self.trans[source]:
                # Check whether there are two transitions with same
                # source state and label
                if len(self.trans[source][label]) > 1:
                    if verbose:
                        print("Too many outgoing transitions from " , source, "labelled by " ,label)
                    return False
        return True


    def is_complete(self,verbose=False):
        """
        :return: True if the automaton is complete, False otherwise
        """
        lettersAreComlplete=True
        
        for source in self.trans:
            # Loop over labels
            letterInTransition= True
            for alpha in self.alphabet:
                found =False

                for label in self.trans[source]:
                   if alpha ==label:
                       found = True

                if not(found) and verbose: print("There is no ", alpha, " transition from", source)  
                letterInTransition =found and letterInTransition

            lettersAreComlplete = lettersAreComlplete and letterInTransition
        return lettersAreComlplete


    def compute_next(self, X, sigma):
        """
        :param X: set of states
        :param sigma: symbol of the alphabet
        :return: a set of states corresponding to one-step successors of X by reading sigma
        """
        res = set()
        if isinstance(X,int):
            return self.trans[X][sigma]
        
        for state in X:
            if state in self.trans:
                if sigma in self.trans[state]:
                    nextState=self.trans[state][sigma]
                    res.update(nextState)
        return res


    def accept(self, word):
        """
        :param word: string on the alphabet
        :return: True if word is accepted, False otw
        """
        X=self.ini
        for i in range(0,len(word)):
            print(word[i])
            X = self.compute_next(X,word[i])
        if X.intersection(self.final)!= set() :
            return True
        return False


    def reachable_states(self):
        """
        Computes the of states reachable from the initial ones
        :return: the set of reachable states
        """
        X=self.ini
        Y= set()
        while X != Y:
            Y=X
            for sigma in self.alphabet:
                X=X.union(self.compute_next(X,sigma))
        return X


    def is_empty(self):
        """
        Checks whether the automaton accepts no word. Proceeds by checking
        whether there exists a final state reachable from an initial one.
        :return: True if the language of the automaton is empty, False otherwise
        """
        return (self.reachable_states().intersection(self.final) == set())


    def intersection(self,other):
        """
        :param other: an automaton
        :return: a new automaton whose language is the intersection
        """
        #we return the product of two automata




        return


    def union(self,other):
        """
        :param other: an automaton
        :return: a new automaton whose language is the union
        """
        
        return

    def product(self,other):
         """
        :param other: an automaton
        :return: a new automaton whose language is the PRODUCT
        """
         currentState=[]
         nextStateWithCurrentLabel=[]
         Sigma = self.alphabet.union(other.alphabet)
         states = []
         trans = {}
         ini = self.ini.union(other.ini)
         final = self.final.union(other.final)
         DictPairTrans={}
         res = Automata(Sigma,set(states),trans,ini,final)
         #we define all states in our automata
         for stateA in self.states:
             for stateB in other.states:
                 states.append((stateA,stateB))
         


         #for every couple state we look for the accepted states

         for state in states:
            for label in self.alphabet:
                
                nextStateWithCurrentLabel=[self.compute_next(state[0],label),other.compute_next(state[1],label)]
                
                DictPairTrans.__setitem__(state,DictPairTrans[state].__setitem__({label:nextStateWithCurrentLabel}))
                print('label',label)
         print(DictPairTrans) 