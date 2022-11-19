# A simple transportation problem 
!pip install ortools
from ortools.linear_solver import pywraplp

c= [
    [300, 550, 700],
    [420, 200, 500],
    [320, 400, 600],
]
S = [1500, 2300, 2850]
D = [2450, 2000, 2200]
n = len(c[0]) # The number of Dealers
m = len(c) # The number of PDCs

solver = pywraplp.Solver("A simple transportation problem", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING )
x = {}
for i in range(m):
  for j in range(n):
    x[i,j] = solver.IntVar(0,solver.infinity(),"")

for i in range(m):
  solver.Add(solver.Sum(x[i,j] for j in range(m)) <= S[i])
for j in range(n):
  solver.Add(solver.Sum(x[i,j]for i in range(n)) >= D[j])
 
objective_terms = []
for i in range(n):
  for j in range(m):
    objective_terms.append(c[i][j]*x[i,j])
solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
  print("Total cost =" , solver.Objective().Value(),'\n')
  for i in range(m):
    for j in range(n):
      print("From PDC %d to Dealer %d: %d" % (i+1, j+1, x[i,j].solution_value()))
else:
  print("No solution found.")
