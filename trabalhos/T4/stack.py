class Stack(list):
    def push(self, __object):
        self.append(__object)

    def isempty(self): return not self