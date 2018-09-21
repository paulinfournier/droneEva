import model
from sympy import symbols

p = symbols('p')

class BiasedCoin(model.AbstractPMC):
    def initial(self):
        return [0,0]

    def next(self, a_state):
        n,t=a_state
        return [p,1-p],[[n+1,t+1],[n,t+1]]

    def end(self, a_state):
        n,t = a_state
        return t==2,n==2