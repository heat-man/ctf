from z3 import *

# Create Z3 variables
a, b, c, d, e, f = Int('a b c d e f')

# Create a Z3 solver
solver = Solver()

# Add the equations to the solver
solver.add(a + b + c + d + e + f == 41)
solver.add(a * b * c * d * e * f == 30030)

# Check if the equations have a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("Solution:")
    print("a =", model[a])
    print("b =", model[b])
    print("c =", model[c])
    print("d =", model[d])
    print("e =", model[e])
    print("f =", model[f])
else:
    print("No solution found.")

