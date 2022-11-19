# Assignment with Task Sizes(time)
# The total size of the tasks performed by each worker has a fixed bound
!pip install ortools
from ortools.linear_solver import pywraplp

costs = [
    [90, 76, 75, 70, 50, 74, 12, 68],
    [35, 85, 55, 65, 48, 101, 70, 83],
    [125, 95, 90, 105, 59, 120, 36, 73],
    [45, 110, 95, 115, 104, 83, 37, 71],
    [60, 105, 80, 75, 59, 62, 93, 88],
    [45, 65, 110, 95, 47, 31, 81, 34],
    [38, 51, 107, 41, 69, 99, 115, 48],
    [47, 85, 57, 71, 92, 77, 109, 36],
    [39, 63, 97, 49, 118, 56, 92, 61],
    [47, 101, 71, 60, 88, 109, 52, 90],
]
num_workers = len(costs)
num_tasks = len(costs[0])
task_sizes = [10, 7, 3, 12, 15, 4, 11, 5]
total_size_max = 15 

solver = pywraplp.Solver("Assignment with Task Sizes",pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
x = {} 
for i in range(num_workers):
  for j in range(num_tasks):
    x[i,j] = solver.IntVar(0,1,'')
    
for i in range(num_workers):
  solver.Add(solver.Sum([task_sizes[j] * x[i,j]for j in range(num_tasks)]) <= total_size_max)
for j in range(num_tasks):
  solver.Add(solver.Sum([x[i,j] for i in range(num_workers)]) ==1)
  
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
