# library for symbolic computation
from sympy import *
from random import random
# defining variables with the symbols function
a, b, c = symbols('a b c')
mu = symbols('mu')
beta1, beta2, beta3 = symbols('beta1 beta2 beta3')
omega1, omega2, omega3 = symbols('omega1 omega2 omega3')

# ignore this, these aren't used anywhere but the print statements right below
da = a*(beta1*(1-a-b-c) + omega3*c - omega1*b - mu)
db = b*(beta2*(1-a-b-c) + omega1*a - omega2*c - mu)
dc = c*(beta3*(1-a-b-c) + omega2*b - omega3*a - mu)

#print(latex(da))
#print(latex(db))
#print(latex(dc))

pprint(da)
pprint(db)
pprint(dc)

# these four matrices were made by hand
# but they could be generated using the three equations above
# probably
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

# solves the system for the given variables
E4 = solve_linear_system(E4, a, b)
E5 = solve_linear_system(E5, b, c)
E6 = solve_linear_system(E6, a, c)

#pprint(E7)
#E7.col_del(3)
#pprint(E7)
#print(latex(E7.eigenvals()))
sol = solve_linear_system(E7, a, b, c)

b1 = random()
b2 = random()
b3 = random()

u = random()

w1 = random()
w2 = random()
w3 = random()

substs = [(mu, u), (beta1, b1), (beta2, b2), (beta3, b3), (omega1, w1), (omega2, w2), (omega3, w3)]

pprint(substs)
pprint(sol[a])
pprint(sol[b])
pprint(sol[c])

# outputs
#print('\n\nE4')
#for key in E4.keys():
#    pprint(E4[key])
#    # can be given in latex as well
#    #print(latex(E4[key]))
#    print()
#
#print('\n\nE5')
#for key in E5.keys():
#    pprint(E5[key])
#    #print(latex(E5[key]))
#    print()
#
#print('\n\nE6')
#for key in E6.keys():
#    pprint(E6[key])
#    #print(latex(E6[key]))
#    print()
#
#
##print('\n\nE7')
##for key in E7.keys():
##    pprint(E7[key])
##    #print(latex(E7[key]))
##    print()
#
#pprint(E7)
