import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from matplotlib.widgets import Slider
from random import random, uniform
from scipy import integrate
from scipy.integrate import odeint
from sympy import *
from sys import argv

def eq(par, init, t0, tn, steps):
    t = np.linspace(t0, tn, steps)

    def fn(y, t):
        a, b, c = y
        u, b1, b2, b3, o1, o2, o3 = par

        da = a*(b1*(1-a-b-c)+o3*c-o1*b-u)
        db = b*(b2*(1-a-b-c)+o1*a-o2*c-u)
        dc = c*(b3*(1-a-b-c)+o2*b-o3*a-u)

        return [da, db, dc]

    ds = odeint(fn, init, t)
    return (ds[:,0], ds[:,1], ds[:,2], t)

dem_pers = [52,46.7, 45.6, 44.4, 43.0, 42.5, 44.5, 44.0, 43.9, 43.2]
rep_pers = [48,35.3, 34.8, 35.2, 34.5, 34.2, 31.1, 30.9, 28.9, 28.0]
oth_pers = [ 100 - (x[0] + x[1]) for x in zip(dem_pers, rep_pers) ]

try:
    u = float(argv[1])
    b1, b2, b3 = float(argv[2]), float(argv[3]), float(argv[4])
    o1, o2, o3 = float(argv[5]), float(argv[6]), float(argv[7])

except:
    u = random()
    b1, b2, b3 = random(), random(), random()
    o1, o2, o3 = random(), random(), random()

an = [ x/100 for x in dem_pers ]
bn = [ x/100 for x in rep_pers ]
cn = [ x/100 for x in oth_pers ]

y0 = [an[0], bn[0], cn[0]]
rates = [u, b1, b2, b3, o1, o2, o3]

a, b, c = symbols('a b c')
mu = symbols('mu')
beta1, beta2, beta3 = symbols('beta1 beta2 beta3')
omega1, omega2, omega3 = symbols('omega1 omega2 omega3')

E4 = Matrix( ((-beta1, -(beta1+omega1), mu-beta1),
              (omega1-beta2, -beta2, mu-beta2))
           )

E5 = Matrix( ((-beta2, -(beta2+omega2), mu-beta2), 
              (omega2-beta3, -beta3, mu-beta3)) 
           )

E6 = Matrix( ((-beta1, omega3-beta1, mu-beta1),
              (-(beta3+omega3), -beta3, mu-beta3))
           )

E7 = Matrix( ((-beta1, -(beta1+omega1), omega3-beta1, mu-beta1),
              (omega1-beta2, -beta2, -(beta2+omega2), mu-beta2),
              (-(beta3+omega3), omega2-beta3, -beta3, mu-beta3))
           )

E1 = 1-mu/beta1
E2 = 1-mu/beta2
E3 = 1-mu/beta3
E4 = solve_linear_system(E4, a, b)
E5 = solve_linear_system(E5, a, c)
E6 = solve_linear_system(E6, b, c)
sol = solve_linear_system(E7, a, b, c)
substs = [(mu, u), (beta1, b1), (beta2, b2), (beta3, b3), (omega1, o1), (omega2, o2), (omega3, o3)]

pprint(substs)
ans1 = sol[a].subs(substs)
ans2 = sol[b].subs(substs)
ans3 = sol[c].subs(substs)

print(ans1)
print(ans2)
print(ans3)

blue_patch = mpatches.Patch(color='blue', label='Party A')
red_patch = mpatches.Patch(color='red', label='Party B')
green_patch = mpatches.Patch(color='green', label='Party C')

f, axarr = plt.subplots(2, 2)
f.suptitle('$\\mu$={:.2f}, $\\beta_1$={:.2f}, $\\beta_2$={:.2f}, $\\beta_3$={:.2f}, $\\omega_1$={:.2f}, $\\omega_2$={:.2f}, $\\omega_3$={:.2f}'.format(rates[0], rates[1], rates[2], rates[3], rates[4], rates[5], rates[6]), fontsize=11, y=1.001)

az, bz, cz, tz = eq(rates, y0, 0, 500, 2000)

axarr[0, 0].plot(az, 'b-')
axarr[0, 0].plot(bz, 'r-')
axarr[0, 0].plot(cz, 'g-')
axarr[0, 0].plot(an, 'bo')
axarr[0, 0].plot(bn, 'ro')
axarr[0, 0].plot(cn, 'go')
axarr[0, 0].legend(framealpha=1,loc='best',prop={'size':5},handles=[blue_patch,red_patch,green_patch])
axarr[0, 0].set_title('Parties Over Time')

####################################

az, bz, cz, tz = eq(rates, y0, 0, 10000, 100000)

#axarr[0, 1].plot([az[-1]], [bz[-1]], 'go')

axarr[0, 1].plot(az, bz)

axarr[0, 1].plot([0], [0], 'ro')
axarr[0, 1].annotate('(0,0,0)', xy=(0,0), textcoords='offset points')

axarr[0, 1].plot([E1.subs(substs)], [0], 'ro')
axarr[0, 1].annotate('(a*,0,0)', xy=(E1.subs(substs),0), textcoords='offset points')

axarr[0, 1].plot([0], [E2.subs(substs)], 'ro')
axarr[0, 1].annotate('(0,b*,0)', xy=(0,E2.subs(substs)), textcoords='offset points')

axarr[0, 1].plot([E4[a].subs(substs)], [E4[b].subs(substs)], 'ro')
axarr[0, 1].annotate('(a*,b*,0)', xy=(E4[a].subs(substs),E4[b].subs(substs)), textcoords='offset points')

axarr[0, 1].plot([ans1], [ans2], 'ro')
axarr[0, 1].annotate('(a*,b*,c*)', xy=(ans1,ans2), textcoords='offset points')

axarr[0, 1].set_title('Party A & B')

####################################

axarr[1, 0].plot(az, cz)

axarr[1, 0].plot([0], [0], 'ro')
axarr[1, 0].annotate('(0,0,0)', xy=(0,0), textcoords='offset points')

axarr[1, 0].plot([E1.subs(substs)], [0], 'ro')
axarr[1, 0].annotate('(a*,0,0)', xy=(E1.subs(substs),0), textcoords='offset points')

axarr[1, 0].plot([0], [E3.subs(substs)], 'ro')
axarr[1, 0].annotate('(0,0,c*)', xy=(0,E3.subs(substs)), textcoords='offset points')

axarr[1, 0].plot([E5[a].subs(substs)], [E5[c].subs(substs)], 'ro')
axarr[1, 0].annotate('(a*,0,c*)', xy=(E5[a].subs(substs),E5[c].subs(substs)), textcoords='offset points')

axarr[1, 0].plot([ans1], [ans3], 'ro')
axarr[1, 0].annotate('(a*,b*,c*)', xy=(ans1,ans3), textcoords='offset points')

axarr[1, 0].set_title('Party A & C')

####################################

axarr[1, 1].plot(bz, cz)

axarr[1, 1].plot([0], [0], 'ro')
axarr[1, 1].annotate('(0,0,0)', xy=(0,0), textcoords='offset points')

axarr[1, 1].plot([E2.subs(substs)], [0], 'ro')
axarr[1, 1].annotate('(0,b*,0)', xy=(E2.subs(substs),0), textcoords='offset points')

axarr[1, 1].plot([0], [E3.subs(substs)], 'ro')
axarr[1, 1].annotate('(0,0,c*)', xy=(0,E3.subs(substs)), textcoords='offset points')

axarr[1, 1].plot([E6[b].subs(substs)], [E6[c].subs(substs)], 'ro')
axarr[1, 1].annotate('(0,b*,c*)', xy=(E6[b].subs(substs),E6[c].subs(substs)), textcoords='offset points')

axarr[1, 1].plot([ans2], [ans3], 'ro')
axarr[1, 1].annotate('(a*,b*,c*)', xy=(ans2,ans3), textcoords='offset points')

axarr[1, 1].set_title('Party B & C')

f.tight_layout()
plt.show()
