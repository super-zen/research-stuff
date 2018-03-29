import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from scipy import integrate
from scipy.integrate import odeint

from random import random, randint

# http://www.sos.ca.gov/elections/voter-registration/voter-registration-statistics
Ns = [743357,765278,783840,786058,789671,802983,830623,839620,850536]
Vs = [480185,494244,496905,514880,515997,525022,532644,535633,543490]
Bs = [160508,163451,160327,165131,152379,157510,155174,155180,146445]
Cs = [153394,152997,149703,154531,146716,169339,167087,166462,167910]

Vn = []
Bn = []
Cn = []
Nn = []
for i in range(len(Ns)):
    Vn.append(Vs[i]/Ns[i])
    Bn.append(Bs[i]/Ns[i])
    Cn.append(Cs[i]/Ns[i])
    Nn.append(Ns[i]/Ns[i])

def eq(par,init,t0,tn,step):
    t = np.linspace(t0,tn,step)
    
    def fn(y,t):
        N, V, B, C = y
        u, b1, b2, t1, t2 = par

        dV = u*N - u*V - b1*B*V/N - b2*C*V/N
        dB = b1*B*V/N + t2*B*C/N - t1*C*B/N - u*B
        dC = b2*C*V/N - t2*B*C/N + t1*C*B/N - u*C
        dN = 0
        #dN = dV + dB + dC # wanted to see what would happen

        return [dN, dV, dB, dC]
  
    ds = integrate.odeint(fn,init,t)
    return (ds[:,0],ds[:,1],ds[:,2],ds[:,3],t)

# number of Republicans in Ventura
B = Bn[0]
# number of Democrats in Ventura
C = Cn[0]
# number of eligible voters in Ventura
V = Vn[0]
# total population of voters in Ventura
N = Nn[0]

# randomize the parameters just to see what happens
# TODO: choose parameters that match reality
u  = random() # rate people join V from N and exit V, B, and C
b1 = random() # rate people join B from V
b2 = random() # rate people join C from V
t1 = random() # rate people join C from B
t2 = random() # rate people join B from C

y0 = [N,V,B,C]
rates = [u,b1,b2,t1,t2]
#rates = [0.16938768950486316, 0.051717135227532296, 0.46443936015610854, 0.15823446058524515, 0.8981081104262618]
#rates = [0.17, 0.052, 0.46, 0.16, 0.9]
#rates = [0.17, 0.052, 0.46, 0.3, 0.9]
#print(rates)

n = 21
#n = 8
N, V, B, C, T = eq(rates,y0,0,n,n)

plt.figure()
yellow_patch = mpatches.Patch(color='yellow', label='Population')
red_patch = mpatches.Patch(color='red', label='Republicans')
green_patch = mpatches.Patch(color='green', label='Democrats')
blue_patch = mpatches.Patch(color='blue', label='Other')

up = mpatches.Patch( color='white',label='mu: {}'.format(rates[0]))
b1p = mpatches.Patch(color='white',label='beta1: {}'.format(rates[1]))
b2p = mpatches.Patch(color='white',label='beta2: {}'.format(rates[2]))
t1p = mpatches.Patch(color='white',label='theta1: {}'.format(rates[3]))
t2p = mpatches.Patch(color='white',label='theta2: {}'.format(rates[4]))

plt.legend(framealpha=0.5,loc='best',handles=[red_patch,green_patch,blue_patch,up,b1p,b2p,t1p,t2p])

x = np.array(range(50))
xs = [ '0{}'.format(i % 100) if i % 100 < 10 else '{}'.format(i % 100) for i in range(1999,2050,2) ]
xt = np.array(xs)
plt.xticks(x,xt)

plt.plot(Vn,'ro')
plt.plot(Bn,'go')
plt.plot(Cn,'bo')

plt.plot(V,'-r')
plt.plot(B,'-g')
plt.plot(C,'-b')

plt.show()


