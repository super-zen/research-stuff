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

def update(val):
    a = a_slider.val
    b = b_slider.val
    c = c_slider.val

    u = u_slider.val

    b1 = b1_slider.val
    b2 = b2_slider.val
    b3 = b3_slider.val

    o1 = o1_slider.val
    o2 = o2_slider.val
    o3 = o3_slider.val

    az, bz, cz, tz = eq([u,b1,b2,b3,o1,o2,o3], [a,b,c], 0, 500, 2000)

    y1.set_ydata(az)
    y2.set_ydata(bz)
    y3.set_ydata(cz)

    y4.set_xdata(az)
    y4.set_ydata(bz)
    y5.set_xdata(az)
    y5.set_ydata(cz)
    y6.set_xdata(bz)
    y6.set_ydata(cz)

    fig.canvas.draw_idle()

##########################################
# Begin ODE Window

fig, axarr = plt.subplots(2, 2)
#axarr[0, 0].axis([0, 500, 0, 1])

pa, pb, pc = .45, .45, .1
u = 0.3
b1, b2, b3 = .5, .5, .5
o1, o2, o3 = .5, .5, .5

az, bz, cz, tz = eq([u,b1,b2,b3,o1,o2,o3], [pa,pb,pc], 0, 500, 2000)

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
ans1 = sol[a].subs(substs)
ans2 = sol[b].subs(substs)
ans3 = sol[c].subs(substs)

y1, = axarr[0, 0].plot(az, 'b-')
y2, = axarr[0, 0].plot(bz, 'r-')
y3, = axarr[0, 0].plot(cz, 'g-')
y4, = axarr[0, 1].plot(az, bz)
y5, = axarr[1, 0].plot(az, cz)
y6, = axarr[1, 1].plot(bz, cz)

##########################################
# Begin Configuration Window

plt.figure()

ax_a = plt.axes( [0.25, 0.55, 0.65, 0.03])
ax_b = plt.axes( [0.25, 0.50, 0.65, 0.03])
ax_c = plt.axes( [0.25, 0.45, 0.65, 0.03])
ax_u = plt.axes( [0.25, 0.40, 0.65, 0.03])
ax_b1 = plt.axes([0.25, 0.35, 0.65, 0.03])
ax_b2 = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_b3 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_o1 = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_o2 = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_o3 = plt.axes([0.25, 0.10, 0.65, 0.03])

a_slider  = Slider(ax_a, 'A', 0, 1, valinit=pa)
b_slider  = Slider(ax_b, 'B', 0, 1, valinit=pb)
c_slider  = Slider(ax_c, 'C', 0, 1, valinit=pc)
u_slider  = Slider(ax_u, 'mu', 0, 1, valinit=u)
b1_slider = Slider(ax_b1, 'beta1', 0, 1, valinit=b1)
b2_slider = Slider(ax_b2, 'beta2', 0, 1, valinit=b2)
b3_slider = Slider(ax_b3, 'beta3', 0, 1, valinit=b3)
o1_slider = Slider(ax_o1, 'omega1', -1, 1, valinit=o1)
o2_slider = Slider(ax_o2, 'omega2', -1, 1, valinit=o2)
o3_slider = Slider(ax_o3, 'omega3', -1, 1, valinit=o3)

a_slider.on_changed(update)
b_slider.on_changed(update)
c_slider.on_changed(update)
u_slider.on_changed(update)
b1_slider.on_changed(update)
b2_slider.on_changed(update)
b3_slider.on_changed(update)
o1_slider.on_changed(update)
o2_slider.on_changed(update)
o3_slider.on_changed(update)

plt.show()
