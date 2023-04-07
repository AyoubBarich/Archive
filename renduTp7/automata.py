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
        for source in X:
            if source in self.trans:
                for label in self.trans[source]:
                    if label in self.trans[source]:
                        for target in self.trans[source][label]:
                            if (label == sigma):
                                res.add(target)
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
        #we check if any of the given automaton are empty
        if self.is_empty:return self
        if other.is_empty:return other
        #we return the product of two automata
        Sigma = self.alphabet.union(other.alphabet)
        states = {(stateA,stateB) for stateA in self.states for stateB in other.states}
        trans = {}
        ini = {(stateA,stateB) for stateA in self.ini for stateB in other.ini}
        final = {(stateA,stateB) for stateA in self.final for stateB in other.final}
        #we create a new automaton 
        inter = Automata(Sigma,states,trans,ini,final)
        print(states)
        #we loop through all states
        for state in states:
            #we check if the each state has a corresponding transition in its original automaton
            if state[0] in self.trans and state[1] in other.trans:
                #we loop through all lables in our alphabet
                for label in Sigma:
                    if label in self.trans[state[0]] and label in other.trans[state[1]]:
                        #we compute the next state with the current label in each Automaton
                        nextStatesA= self.compute_next(set(state[0]),label)
                        nextStatesB= other.compute_next(set(state[1]),label)
                        nextStatesInInter = {(nextA,nextB) for nextA in nextStatesA for nextB in nextStatesB}

                    for trans in nextStatesInInter:
                        inter.add_transition(state,label,nextStatesInInter)
        return inter
    


    def union(self,other):
        """
        :param other: an automaton
        :return: a new automaton whose language is the union
        """
        if self.is_empty(): return other
        if other.is_empty(): return self

        Sigma = self.alphabet.union(other.alphabet)
        states = {(stateA,0) for stateA in self.states }|{(stateB,1)for stateB in other.states}
        trans = {}
        ini = {(stateA,0) for stateA in self.ini }|{(stateB,1)for stateB in other.ini}
        final = {(stateA,0) for stateA in self.final} |{(stateB ,1)for stateB in other.final}
    
        res = Automata(Sigma,states,trans,ini,final)

        #for every couple state we look for the accepted states
        for state in states:
            if state[1] == 0 :    #we transcript all the state of our first automat to the result 
                if state[0] in self.trans:
                    for label in self.trans[state[0]]:
                        if label in self.trans[state[0]]:
                            for target in self.trans[state[0]][label]:
                                res.add_transition(state, label, (target,0))
            if state[1]==1:   #we transcript all the state of our seconde automat to the result 
                if state[0] in self.trans:
                    for label in self.trans[state[0]]:
                        if label in self.trans[state[0]]:
                            for target in self.trans[state[0]][label]:
                                res.add_transition(state, label, (target,1))

        return res
    
    def complement_DFA(self):
        """
        :return:the complement of this automaton
        """
        res= self
        res.final={(fin) for fin in (self.states.remove(self.final))}
        return res
    
    def check_inclusion_DFA(self,other):

        """
        :param:an other automata
        :return:true if self is included in other
        """
        return other.complement_DFA().intersection(self).is_empty()
    
    def check_equivalence_DFA(self,other):
        """
        :param: an other automata
        :return: true if self is equivalente to other
        """
        return self.check_inclusion_DFA(other) and other.check_inclusion_DFA(self)
        
    def miror(self):
        """
        :param: 
        :return: the mirori of the current automata
        """
        
        
        newTrans={}
        for state in self.states:
            #we intilize all transitions to empty
            newTrans[state]={}
            for label in self.alphabet:
                newTrans[state][label]=set()
        for state in self.trans:
                for label in self.trans[state]:
                    for target in self.trans[state][label]:
                        newTrans[target][label].add(state)  
                        print(newTrans)   
        return Automata(self.alphabet,self.states,newTrans,self.final,self.ini)
    
    def co_reachable_states(self):
        """
        :param:
        :return: set of co reachable states
        """
        return self.miror().reachable_states()
    
    def useful_states(self):
        """
        :param:
        :return: set of useful states
        """
        return (self.reachable_states()).intersection(self.co_reachable_states())
    

    def trim(self):
        """
        :param:
        :return: Automaton with only useful state
        """
        newTrans={}
        useful = self.useful_states()
        for state in useful:
            #we intilize all transitions to empty
            newTrans[state]={}
            for label in self.alphabet:
                newTrans[state][label]=set()

        for state in self.trans:
            if state in useful:
                for label in self.trans[state]:
                    for target in self.trans[state][label]:
                        if target in useful:
                            newTrans[state][label].add(target)
        return Automata(self.alphabet,self.useful_states,newTrans,(self.ini).intersection(useful),self.final.intersection(useful))
        
            
    def determinize(self):
        """
        param: self
        return: returns a the equivalent deterministic aytomaton to self
        
        """
        #we initialze our determinitic automaton
        sigma = self.alphabet
        ini = {0}
        trans= {}
        final =set()
        explored = [self.ini]
        wait = []
        #our waiting list that contants (index of our state ,label )
        for sig in self.alphabet:
            wait.append((0,sig))
        #we go through all the stetse of our automaton and we apply the determize algorithm
        while wait != []:
            #we extract the first element in the waiting list
            element =wait.pop()
            #we store the values in there respective variables
            Stateindex =element[0]
            Statealpha = element[1]
            #we compute the next state
            Y =self.compute_next(explored[Stateindex],Statealpha)
            #we add the the explored states to our list and we remove it from the waiting list
            if Y not in explored :
                explored.append(Y)
                addition = [(explored.index(Y),sig) for sig in self.alphabet]
                wait = wait + addition
            #we chekc if we can add our next state to our transition dictionnary
            if not(Stateindex in trans.keys()):
                trans[Stateindex]={}
            if not(Statealpha in trans[Stateindex]):
                trans[Stateindex][Statealpha]=set()
            trans[Stateindex][Statealpha].add(explored.index(Y))
        #we add all the final states
        for X in explored:
            if not(X in self.final):
                final.add(explored.index(X))
        B=Automata(sigma,explored,trans,ini,final)

        return B
   
    def check_inclusion(self,other):
        """
        param: other automaton
        return: returns true if self is included in other
        
        """
        return self.determinize().check_inclusion_DFA(other.determinize())
        
    def check_equivalence(self,other):
        
        """
        param: other automaton
        return: returns true if self is equivalent to other   
        
        """
        return self.determinize().check_equivalence_DFA(other.determinize())