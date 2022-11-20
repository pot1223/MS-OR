!pip install ortools
from ortools.linear_solver import pywraplp

# data
depot = [1, 2, 3, 4, 5]
center = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
construction = [1000, 500, 1500, 300, 800]
capacity =[200, 105, 400, 50, 500]
cost = [
    [38, 43, 16, 24, 32, 14, 42, 35, 15, 40, 22, 38],
    [26, 35, 37, 10, 37, 27, 49, 13, 17, 37, 49, 18],
    [42, 19, 19, 18, 22, 46, 10, 13, 13, 27, 47, 17],
    [47, 26, 32, 22, 33, 40, 31, 35, 26, 33, 33, 31],
    [42, 25, 18, 49, 39, 21, 22, 39, 50, 29, 10, 10],
]
demand = [100, 150, 80, 50, 40, 10, 200, 100, 30, 20, 14, 20]

# Definition solver
solver = pywraplp.Solver("Facility location problem", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)

# Decision variable
x = {}
for i in depot:
  for j in center:
    x[i, j] = solver.IntVar(0, 1, "")
s = {} 
for i in depot:
  for j in center:
    s[i, j] = solver.IntVar(0, solver.infinity(), "")
    
# constraints
for i in depot:
  solver.Add(solver.Sum([s[i, j] for j in center]) <= capacity[i-1])

for j in center:
  solver.Add(solver.Sum([s[i, j] for i in depot]) >= demand[j-1])

for i in depot:
  for j in center:
    solver.Add(s[i, j] <= demand[j-1]*x[i, j]) # x[i, j] 가 0 이면 s[i, j]도 0이다
    
objective_terms =[]
for i in depot:
  for j in center:
    objective_terms.append(s[i, j] * cost[i-1][j-1])
    # objective_terms.append(x[i,j]* construction[i-1])  고정 건설 비용을 어떻게 활용해야 할지 모르겠음 
