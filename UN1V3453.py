astronomers = []

#-----------------------------------------------------------------------------
# 🛸 SPACETIME 🧿
import autograd.numpy as np
from autograd import grad
def f(x):
    return x
def g(y):
    return y
def h(z):
    return z
def i(t):
    return t
f_primex = grad(f)
f_primey = grad(g)
f_primez = grad(h)
f_primet = grad(i)
x = 1.0
print(f_prime(x))  # Approx: 2 + cos(1)
spacetime = []
# 🌌 SPACETIME 🕋
# ----------------------------------------------------------------------------

earth = []
moon = []
solarsystems = []
blackholes = []

tools = [spacetime]
objects = [blackholes, solarsystems]

universe = [astronomers, objects, tools]
