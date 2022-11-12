!pip install ortools
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver("glassVenture",pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

x = solver.NumVar(0,solver.infinity(),"output of product1")
y = solver.NumVar(0,solver.infinity(),"output of product2")

solver.Add(x<=4)
solver.Add(y<=6)
solver.Add(3*x+2*y <= 18)

solver.Maximize(3000*x + 5000*y)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
  print("Solution:")
  print("Object value =", solver.Objective().Value())
  print("x=", x.solution_value())
  print("y=", y.solution_value())
else:
  print("The problem does not have an optimal solution")
