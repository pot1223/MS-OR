# Assignment with Teams of Workers 
# Six workers are divide into two teams, and each team can perform at most two tasks

!pip install ortools
from ortools.linear_solver import pywraplp

costs = [
    [90, 76, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 105],
    [45, 110, 95, 115],
    [60, 105, 80,75],
    [45, 65, 110, 95],
]
num_workers = len(costs)
num_tasks = len(costs[0])

team1 = [0, 2, 4]
team2 = [1, 3, 5]
team_max = 2 

solver = pywraplp.Solver("Assignment with Teams of Workers",pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
x = {} 
for i in range(num_workers):
  for j in range(num_tasks):
    x[i,j] = solver.IntVar(0, 1 ,"")
    
for i in range(num_workers):
  solver.Add(solver.Sum([x[i,j] for j in range(num_tasks)])<=1)
for j in range(num_tasks):
  solver.Add(solver.Sum([x[i,j] for i in range(num_workers)]) == 1)
team1_tasks = [] 
for i in team1:
  for j in range(num_tasks):
    team1_tasks.append(x[i,j])
solver.Add(solver.Sum(team1_tasks) <= team_max)
team2_tasks = []
for i in team2:
  for j in range(num_tasks):
    team2_tasks.append(x[i,j])
solver.Add(solver.Sum(team2_tasks) <= team_max)

objective_terms = []
for i in range(num_workers):
  for j in range(num_tasks):
    objective_terms.append(costs[i][j]*x[i,j])
solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
  print("Total cost= ", solver.Objective().Value())
  for i in range(num_workers):
    for j in range(num_tasks):
      if x[i,j].solution_value() > 0.5:
        print("worker %d assigned to task %d. Cost = %d" % (i, j , costs[i][j]))
else:
  print("No solution found.")
