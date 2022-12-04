!pip install ortools
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver("PERT toast", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

t = [solver.NumVar(0, solver.infinity(),'') for i in range(1, 12)]
y = [solver.NumVar(0, solver.infinity(),'') for j in ['A','D','G','H','I','J']]

solver.Add(t[1]-t[0] >= 0.5 -y[0])
solver.Add(t[2]-t[0] >= (3.4 / 6))
solver.Add(t[3]-t[0] >= 10)
solver.Add(t[4]-t[1]>= ((9.3/6)-y[1]))
solver.Add(t[5]-t[2]>= (13.9/6))
solver.Add(t[6]-t[2]>=(33.4/6))
solver.Add(t[7]-t[3]>=((2.0/6)-y[4]))
solver.Add(t[8]-t[4]>=0)
solver.Add(t[8]-t[5]>=((2.9/6)-y[2]))
solver.Add(t[9]-t[8]>=0)
solver.Add(t[9]-t[6]>=((4.5/6)-y[3]))
solver.Add(t[9]-t[7]>=0)
solver.Add(t[10]-t[9]>=((6.7/6)-y[5]))
solver.Add(solver.Sum([i for i in y])<=2)
for i in y:
  solver.Add(i<=1.5)

solver.Minimize(t[10])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
  print("Solution:")
  print("Object value time=", solver.Objective().Value())
  for j in range(len(y)):
    if y[j].solution_value() > 0:
      print(f"Shortening time y[{j}] : {y[j].solution_value()}")
  for i in range(len(t)):
    print(f"t{i+1}={t[i].solution_value()}")
else:
  print("The problem does not have an optimal solution")
