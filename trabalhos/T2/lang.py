import copy

class Language:
    """
    Classe para representar uma linguagem
    """
    def __init__(self, terminals, no_terminals, void_symbol='#', **rules: dict):
        self.productions = {}
        for word, rules in rules.items():
            self.productions[word] = rules
            setattr(self, word, rules)
        
        self.terminals = terminals
        self.no_terminals = no_terminals
        self.void = void_symbol 

        self._first, self._follow = {}, {}


    def __repr__(self) -> str:
        return self.productions.__str__()


    def _remove_left_single_recursion(self, word, inplace=False):
        new_lang = copy.deepcopy(self)
    
        WORD_LINE = f'{word}\''

        productions = getattr(new_lang, word)
        new_word_productions = []
        word_line_productions = []
        for prod in productions:
            if prod[0] == word:
                word_line_productions.append(prod[1:]+[WORD_LINE])
            else:
                new_word_productions.append(prod+[WORD_LINE])
        word_line_productions.append([self.void])

        new_lang.productions[word] = new_word_productions
        new_lang.productions[WORD_LINE] = word_line_productions

        setattr(new_lang, word, new_word_productions)
        setattr(new_lang, WORD_LINE, word_line_productions)

        if not inplace:
            return new_lang
        
        self.productions = new_lang.productions
        for word, productions in new_lang.productions.items():
            setattr(self, word, productions)
    

    def remove_left_recursion(self, word = None, inplace=False):
        if word is not None:
            return self._remove_left_single_recursion(word, inplace)
        
        new_lang = copy.deepcopy(self)

        for word_ in new_lang.productions.keys():
            if self.isrecursive(word_):
                new_lang._remove_left_single_recursion(word_, True)
        
        if not inplace:
            return new_lang
        
        self.productions = new_lang.productions
        for word, productions in new_lang.productions.items():
            setattr(self, word, productions)
        return self
    

    def _check_recursion(self, word, first_word):
        if first_word not in self.productions:
            return False
        if first_word == word:
            return True
        for prod in self.productions[first_word]:
            if prod[0] == first_word:
                return False
            if prod[0] in self.productions:
                return self._check_recursion(word, prod[0])
        return False


    def isrecursive(self, word: str) -> bool:
        return True in [
            self._check_recursion(word, prod[0])
            for prod in self.productions[word]]


    def first(self, X):
        first_ = []
        if X in self.terminals:
            return [X]
        for production in self.productions[X]:
            if production[0] not in self.productions:
                first_.append(production[0])
            else:
                first_ += self.first(production[0])
        return first_