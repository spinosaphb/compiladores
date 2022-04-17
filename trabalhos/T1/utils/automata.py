"""
Módulo para automatos
"""

try:
    from graphviz import Digraph
except ImportError as ie :
    raise ImportError("""
        Módulo graphviz é necessário para utilizar todas as funções
        Execute: pip install graphviz
    """) from ie

import re

class FA():
    """
    Representa um automato NFA, exemplo:

    a1 = Automato(
        q0 = {'a': ('q0', 'q1'), 'b':'q0'} , 
        q1 = {'b': 'q2'}
    )
    """

    def __init__(self, initial = None, finals:set = None, **kwargs) -> None:
        self.fa = {}
        self._STATES = set()
        self._INPUTS = set()

        if initial is None:
            raise RuntimeError('É preciso fornecer o estado inicial')

        self.__handle_states(**kwargs)

        self._FINALS = set({finals}) if type(finals) is str else set(finals)

        if hasattr(self, initial):
            self.initial = initial
        else:
            raise RuntimeError("Forneça um estado inicial válido")
    
    def __handle_states(self, **kwargs):
        def __validade_states(state: dict):
            for input_ in state.keys():
                self._INPUTS.add(input_)
                if not isinstance(state[input_], set):
                    state[input_] = set([state[input_]])

        for state, transictions in kwargs.items():
            self._STATES.add(state)
            __validade_states(transictions)
            self.fa[state] = transictions
            setattr(self, state, transictions)


    def __repr__(self):
        str_ = ""
        for state in self.fa.keys():
            str_ += state + " -> " + str(getattr(self, state))
            str_ += '\n'
        return str_


    def edge(self, state, input_):
        """
        Retorna os estados alcançados a partir de state com input
        """
        try:
            return getattr(self, state)[input_]
        except KeyError:
            return set()


    def closure(self, s_state: str, states=None):
        """
        Retorna todos os estados alcançáveis a partir do conjunto S, sem
        consumir caractere de entrada.
        """
        if states is None:
            states = []
        if s_state in states:
            return {}

        state = getattr(self, s_state)
        states.append(s_state)
        c_set:set = state[''] if '' in state.keys() else set()
        c_subsets = set()
        for c_state in c_set:
            c_subsets = c_subsets.union(self.closure(c_state, states))
        return c_set.union(c_subsets.union({s_state}))


    def DFAedge(self, d, c):
        """
        Retorna todos os estados alcançáveis a partir de s, consumindo c.
        """
        edges = set()
        for state in d:
            if c in getattr(self, state).keys(): 
                edges = edges.union(getattr(self, state)[c])
        
        closures = set()
        for edge in edges:
            closures = closures.union(self.closure(edge))
        return closures


    def __find_states(
        self,
        current_state,
        states):

        new_states = []

        for state in current_state:
            for input_ in self._INPUTS.difference({''}):
                if input_ not in states[current_state].keys():
                    states[current_state][input_] = set()
                if input_ in getattr(self, state).keys():
                    states_set = getattr(self, state)[input_]
                    closures = set()
                    for state_ in states_set:
                        closures = closures.union(self.closure(state_))
                    state_from_input = states[current_state][input_].union(
                        states_set.union(closures) 
                    )
                    if state_from_input not in list(map(set, states.keys())):
                        new_states.append(state_from_input)
                    states[current_state][input_] = state_from_input
        
        return new_states


    def nfa2dfa(self):
        """
        Converte o NFA para dfa
        """
        states: dict = {}
        init_state_set = tuple(self.closure(self.initial))
        states[init_state_set] = {}      

        processed_states = []
        new_states = [None]
        
        while(len(new_states) > 0):
            new_states = []
            for state in states.keys():
                if state not in processed_states:
                    new_states += self.__find_states(state, states)
                    processed_states.append(state)
 
            for new_state in set(map(frozenset, new_states)):
                states[tuple(new_state)] = {}

        check_final = lambda state_set_: \
            True in map(lambda state_: state_ in self._FINALS, state_set_)

        final_states = [
            processed_state
            for processed_state in processed_states
            if check_final(processed_state)
        ]        

        ## Transformando a parte interna em tupla (estados destino)
        states = {
            str(state): {
                terminal: tuple(target)
                for terminal, target in trans.items()
            }  
            for state, trans in states.items()
        }

        return states, init_state_set, final_states 
        # return NFA(
        #     initial=str(init_state_set),
        #     finals=final_states,
        #     kwargs=states
        # )


    def __reajust_set(self, set_: tuple):
        """
        Reajusta o conjunto para nao ter permutações
        """
        str_set_state2set = lambda s: set(re.sub("['()]","", s).split(', '))
        list_finals_set = list(map(str_set_state2set, self._FINALS))  
        for final_set in list_finals_set:
            if set(set_) == final_set:
                return tuple(final_set)   
        return set_

    def make_automata_graph(self):
        """
        Desenha automato
        """

        graph = Digraph()

        for state in self._STATES:
            if state not in self._FINALS:
                graph.attr('node', shape='circle')
                graph.node(str(state))
            else:
                graph.attr('node', shape='doublecircle')
                graph.node(str(state))


        graph.attr('node', shape='none')
        graph.node('')
        graph.edge('', self.initial)

        for state in self._STATES:
            for input_ in self._INPUTS:        
                values = self.edge(state, input_)
                if len(values) == 0:
                    continue
                for value in values:
                    if isinstance(value, tuple):
                        value = str(self.__reajust_set(value))  
                    graph.edge(state, value, label=('ε', input_)[input_ != ''])

        #raph.render('nfa', view=True)
        return graph
