from sympy import *
from sympy.solvers.solveset import linsolve

init_printing()

a, b, c, beta1, beta2, beta3, omega1, omega2, omega3, mu = symbols('a,b,c,beta1,beta2,beta3,omega1,omega2,omega3,mu')

#f1 = a*(beta1*(1-a-b-c)+omega3*c-omega1*b-mu)
#f2 = b*(beta2*(1-a-b-c)+omega1*a-omega2*c-mu)
#f3 = c*(beta3*(1-a-b-c)+omega2*b-omega3*a-mu)

f1 = beta1*(a-a**2-a*b-a*c)+omega3*a*c-omega1*a*b-a*mu
f2 = beta2*(b-a*b-b**2-b*c)+omega1*a*b-omega2*b*c-b*mu
f3 = beta3*(c-a*c-b*c-c**2)+omega2*b*c-omega3*a*c-c*mu

soln = linsolve([f1, f2, f3], (a, b, c))

fs = Matrix([f1, f2, f3])
wrts = Matrix([a, b, c])

jacobian = fs.jacobian(wrts)

newjacobian = jacobian.subs(a, 0).subs(b, 0).subs(c, 0)

eigvaldict = newjacobian.eigenvals()
eigvals = [ key for key in eigvaldict.keys() ]

for val in eigvals:
    assert (newjacobian-val*eye(3)).expand().det() == 0

print('It worked!')
