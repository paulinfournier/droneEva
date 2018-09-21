from abc import ABC, abstractmethod
from numpy.random import choice

def norm_proba(l):
    """
    normalize a vector of probability.
    :param l: the vector of probability with (may be) parametric probabilities
    :return: the normalized float vector
    """

    prob = 1
    nb_param = 0
    for p in l:
        if isinstance(p, float):
            prob -= p
        else:
            nb_param += 1
    if nb_param == 0:
        return l
    norm_prob = prob / nb_param
    return [p if isinstance(p, float) else norm_prob for p in l]


class AbstractPMC(ABC):

    @abstractmethod
    def initial(self):
        """
        Must be implemented.
        :return: The initial state of the pmc
        """
        pass

    @abstractmethod
    def next(self, a_state):
        """
        Must be implemented.
        Return a list of successor states with their probability.
        :param a_state: The state.
        :return: It's successors in the format [p1,p2,p3,...],[s1,s2,s3,...]
        """
        pass

    @abstractmethod
    def end(self, a_state):
        """
        Must be implemented.
        Return whether the state is an end state and whether it is good or not.
        :param a_state: The state.
        :return: End state or not, good or not in the format: [end?,good?]
        """
        pass

    def simu1(self):
        """
        Simulate the pmc until an end state. Return the corrected parametric probability of the run either in the first
        component if the end state is good or in the second if the end state is bad.
        :return: [p,0] if good end state of [0,p] otherwise
        """
        proba = 1
        state = self.initial()
        finished, good = self.end(state)
        while not finished:
            probabilities, successors = self.next(state)
            norm_p = norm_proba(probabilities)
            succ = choice(range(len(norm_p)), p=norm_p)
            state = successors[succ]
            if probabilities[succ] != norm_p[succ]:
                proba *= probabilities[succ] / norm_p[succ]
            finished, good = self.end(state)
        if good:
            return [proba, 0]
        else:
            return [0, proba]


    def simulate(self,n):
        """
        Simulate the pmc n times returning the parametric probability, the parametric size of the confidence interval,
         the parametric probability of not reaching and teh parametric size of the IC [p,sigma_p,q,sigma_q].
        Note that p should be close of 1-q. If it is not the case increase n.
        :param n: number of simulations (square numbers are better for readability)
        :return: [p,sigma,q,sigma']
        """

        p = 0
        q = 0
        sigma_p = 0
        sigma_q = 0
        for _ in range(n):
            g,b = self.simu1()
            p += g
            q += b
            sigma_p += g*g
            sigma_q += b*b
        p /= n
        q /= n
        icw_p = 3.92 * ((1/(n-1) * sigma_p - n/(n-1) * p * p)/n) ** (1/2)
        icw_q = 3.92 * ((1/(n-1) * sigma_q - n/(n-1) * q * q)/n) ** (1/2)

        return [p,icw_p,q,icw_q]