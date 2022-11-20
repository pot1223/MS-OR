# Sunocoil

!pip install ortools
from ortools.linear_solver import pywraplp

# data 
P = ["G80", "G90", "G93", "Diesel", "EnginOil"]
T = [1, 2, 3, 4, 5, 6, 7, 8, 9]
demand = [1200, 700 ,1000, 450, 1200]
capacity = [500, 400, 400, 600, 600, 900, 800, 800, 800]
currentLiquid = [0, 100, 0, 0, 0, 0, 300, 0, 0]
a = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0]
]

num_products = len(P)
num_tanks = len(T)

# solver definition
solver = pywraplp.Solver("Sunocoil Bin-packing",pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)

# Decision Variable
x = {}
for i in range(num_products):
  for j in range(num_tanks):
    x[i, j] = solver.IntVar(0, 1, "")
y = {}
for i in range(num_products):
  for j in range(num_tanks):
    y[i, j] = solver.IntVar(0, solver.infinity(), "")

# constraints    
for i in range(num_products):
  solver.Add(solver.Sum([y[i, j] for j in range(num_tanks)]) >= demand[i])

for j in range(num_tanks):
  solver.Add(solver.Sum([y[i, j] for i in range(num_products)]) <= capacity[j] - currentLiquid[j])
  solver.Add(solver.Sum([x[i, j] for i in  range(num_products)]) <= 1)

for i in range(num_products):
  for j in range(num_tanks):
    solver.Add(x[i, j] >= a[i][j])
    solver.Add(y[i ,j] <= (capacity[j]-currentLiquid[j]) * x[i, j])

# objective funciton
objective_terms = []
for i in range(num_products):
  for j in range(num_tanks):
    objective_terms.append(x[i, j])
solver.Minimize(solver.Sum(objective_terms))

# run 
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
  for j in range(num_tanks):
    print("\n[Tank ", j+1 ,"]")
    for i in range(num_products):
      if y[i, j].solution_value() > 0.5:
        print("Add ",y[i, j].solution_value()," gallons of ", P[i], " in tank ", T[j])
  print("\nThe total number of tanks used is: ", solver.Objective().Value())
else:
  print("The problem does not have an optimal solution.")
    
    
