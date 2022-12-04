!pip install ortools
from ortools.linear_solver import pywraplp 

solver = pywraplp.Solver("RELIABLE",pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

t = [solver.NumVar(0, solver.infinity(),'') for i in range(1,16)] # 노드 개수 

solver.Add(t[1]-t[0] >= 2)
solver.Add(t[2]-t[1] >= 4)
solver.Add(t[3]-t[2] >= 10)
solver.Add(t[4]-t[3] >= 6)
solver.Add(t[5]-t[3] >= 4)
solver.Add(t[6]-t[3] >= 7)
solver.Add(t[7]-t[4] >= 7)
solver.Add(t[7]-t[5] >= 0) # dummy activity
solver.Add(t[8]-t[5] >= 5)
solver.Add(t[8]-t[6] >= 0)
solver.Add(t[9]-t[7] >= 9)
solver.Add(t[13]-t[9] >= 2)
solver.Add(t[10]-t[8] >= 8)
solver.Add(t[11]-t[10] >= 5)
solver.Add(t[12]-t[10] >= 4)
solver.Add(t[12]-t[11] >= 0) # dummy activity
solver.Add(t[14]-t[11] >= 6)
solver.Add(t[14]-t[13] >= 0) # dummy activity

solver.Minimize(t[14])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
  print("Solution:")
  print("Object value time=", solver.Objective().Value())
  for i in range(len(t)):
    print(f"t{i+1}={t[i].solution_value()}")
else:
  print("The problem does not have an optimal solution")
