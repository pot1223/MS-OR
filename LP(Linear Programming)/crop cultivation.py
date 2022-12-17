!pip install ortools
from ortools.linear_solver import pywraplp 

solver = pywraplp.Solver("crop cultivation", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Data
crops = ["Wheat","Potatoes","Corn"]
farms = [1, 2, 3]
farmsArea = [2500, 4800, 2800]
farmsWater = [6954000, 7942000, 5471000]
cropsMaximumAcres = [2300, 3200, 2500]
cropsWater = [3500, 4000, 4500]
Yield = [450, 460, 510]

# Decision Variable 
A= {}
for i in crops:
  for j in farms:
    A[(i,j)] = solver.NumVar(0,solver.infinity(),'A_%s_%i' % (i,j))
    
# constraints
k = 0 
for i in crops:
  solver.Add(solver.Sum([A[i, j] for j in farms]) <= cropsMaximumAcres[k])
  k += 1 

for j in farms:
  solver.Add(solver.Sum(c*A[i, j] for i, c in zip(crops,cropsWater)) <= farmsWater[j-1])

for j in farms:
  solver.Add(solver.Sum([A[i, j] for i in crops]) <= farmsArea[j-1])

solver.Add(A["Wheat",2] == 0)

solver.Add(0.9*A["Wheat",1]+(-1)*A["Potatoes",1]+(-1)*A["Corn",1] >= 0)

# Objective function
objective = solver.Objective()
k = 0 
for i in crops: 
  for j in farms:
    objective.SetCoefficient(A[(i, j)], Yield[k])
  k += 1 
objective.SetMaximization()

# solution 
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
  print("Solution:")
  print("Object value(수익) =", solver.Objective().Value(),"$")
  for i in crops:
    for j in farms:
      print(f"{i} Crops in Farm {j} : {A[i,j].solution_value()}(Acres)")
else:
  print("The problem does not have an optimal solution")
