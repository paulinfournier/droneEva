import biasedCoin
import drone
from sympy import symbols

ProbaFilter0, ProbaFilter1, ProbaFilter2, ProbaFilter3, ProbaFilter4 = symbols(
    'ProbaFilter0,ProbaFilter1,ProbaFilter2,ProbaFilter3,ProbaFilter4')

coin = biasedCoin.BiasedCoin()
dro = drone.Drone()



# p,icw_p,q,icw_q = coin.simulate(1000)
#
# print(p)
# print(icw_p)
# print(q)


p,icw_p,q,icw_q = dro.simulate(10000)

print("proba =")
print(p)

print("proba valued")
print(p.subs({ProbaFilter0:0.30, ProbaFilter1:0.26, ProbaFilter2:0.20, ProbaFilter3:0.14, ProbaFilter4:0.10}))

print("icw = ")
print(icw_p)


print("icw valued")
print(icw_p.subs({ProbaFilter0:0.30, ProbaFilter1:0.26, ProbaFilter2:0.20, ProbaFilter3:0.14, ProbaFilter4:0.10}))
#print(q)