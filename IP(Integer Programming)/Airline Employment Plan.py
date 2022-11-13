!pip install ortools
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver("Airline Employment Plan",pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)

Employments=[
    ['Mon',19],
    ['Tue',17],
    ['Wed',15],
    ['Thr',16],
    ['Fri',18],
    ['Sat',20],
    ['Sun',24]
]

x = [solver.IntVar(0, solver.infinity(),Employment[0])for Employment in Employments]
print(f"Number of variables = {solver.NumVariables()}")

solver.Add(x[0] + x[3] + x[4] + x[5] + x[6] >= 19)
solver.Add(x[0] + x[1] + x[4] + x[5] + x[6] >= 17)
solver.Add(x[0] + x[1] + x[2] + x[5] + x[6] >= 15)
solver.Add(x[0] + x[1] + x[2] + x[3] + x[6] >= 16)
solver.Add(x[0] + x[1] + x[2] + x[3] + x[4] >= 18)
solver.Add(x[1] + x[2] + x[3] + x[4] + x[5] >= 20)
solver.Add(x[2] + x[3] + x[4] + x[5] + x[6] >= 24)

obj = solver.Objective()
for i in range(len(x)):
  obj.SetCoefficient(x[i],1)
  
status = solver.Solve()
if status != solver.OPTIMAL:
  print("The problem does not have an optimal solution!")
  if status == solver.FEASIBLE:
    print("A potentially suboptimal solution was found.")
  else:
    print("The solver could not solve the problem.")
    exit(1)
if status == pywraplp.Solver.OPTIMAL:
  print("Solution:")
  print("Objective value =", solver.Objective().Value())
  for j in range(0,len(x)):
    print(f"{x[j]} =",x[j].solution_value())
else:
  print("The problem does not have an optimal solution")

print("\nAdvanced usage:")
print("Problem solved in ",solver.wall_time(),' milliseconds')
print("Problem solved in ", solver.iterations(),' iterations')
