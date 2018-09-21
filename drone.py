import model
from sympy import symbols

ProbaFilter0, ProbaFilter1, ProbaFilter2, ProbaFilter3, ProbaFilter4 = \
    symbols('ProbaFilter0,ProbaFilter1,ProbaFilter2,ProbaFilter3,ProbaFilter4')

DistanceZoneSecurity0, DistanceZoneSecurity1 = 30, 50

frequency = 1
Time = 5

DistanceZoneFilter_ProbaFilter = [[20, ProbaFilter0], [30, ProbaFilter1], [50, ProbaFilter2], [100, ProbaFilter3]]


def calculeProba(LastCorrection, times):
    #print(LastCorrection)
    global DistanceZoneSecurity0, DistanceZoneSecurity1
    global DistanceZoneFilter_ProbaFilter
    global frequency, Time, ProbaFilter4
    ProbaZoneSecurity0 = 0
    ProbaZoneSecurity1 = 0
    ProbaZoneSecurity2 = 0
    proportion = frequency / (Time - frequency * times)
    for dzf, pf in DistanceZoneFilter_ProbaFilter:
        dzf_p = (dzf + LastCorrection) * proportion
        dzf_m = (dzf - LastCorrection) * proportion

        if dzf_p <= DistanceZoneSecurity0:
            ProbaZoneSecurity0 += pf / 2
        elif dzf_p <= DistanceZoneSecurity1:
            ProbaZoneSecurity1 += pf / 2
        else:
            ProbaZoneSecurity2 += pf / 2

        if dzf_m <= DistanceZoneSecurity0:
            ProbaZoneSecurity0 += pf / 2
        elif dzf_m <= DistanceZoneSecurity1:
            ProbaZoneSecurity1 += pf / 2
        else:
            ProbaZoneSecurity2 += pf / 2

    ProbaZoneSecurity2 += ProbaFilter4

    #print([ProbaZoneSecurity0, ProbaZoneSecurity1, ProbaZoneSecurity2])
    return [ProbaZoneSecurity0, ProbaZoneSecurity1, ProbaZoneSecurity2]


class Drone(model.AbstractPMC):
    """
    States of drone are represented as:
    [zoneSecurity, lastCorrection, times]
    """

    def initial(self):
        """
        initially :
        the security zone is 0
        There are no last correction (0)
        The time is 0
        :return: [0,0,0]
        """
        return [0, 0, 0]

    def next(self, a_state):
        zoneSecurity, lastCorrection, times = a_state
        ProbaZoneSecurity = calculeProba(lastCorrection, times)
        return ProbaZoneSecurity, [
            [0, 0, times + 1],
            [1, DistanceZoneSecurity0, times + 1],
            [2, DistanceZoneSecurity1, times + 1]
        ]

    def end(self, a_state):
        zoneSecurity, lastCorrection, times = a_state
        return [(times >= Time / frequency) or zoneSecurity == 2, zoneSecurity == 2]
