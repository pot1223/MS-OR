# How to represent "assigning" in a mathematical way? 
# xij = 1 or 0 (assigning Worker i to Task j / i = 0,1,2,3,4 / j = 0,1,2,3)

!pip install ortools
from ortools.linear_solver import pywraplp

costs = [
    [90, 80, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 95],
    [45, 110, 95, 115],
    [50, 100, 90, 100],
]

num_workers = len(costs) 
num_tasks = len(costs[0])

solver = pywraplp.Solver("Assigning worker to tasks",pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)

x = {}
for i in range(num_workers):
  for j in range(num_tasks):
    x[i,j] = solver.IntVar(0,1,"") # xij를 딕셔너리 형태로 표현 (i,j) : 변수 
    

for i in range(num_workers):
  tmp = []
  for j in range(num_tasks):
    tmp.append(x[i,j])
  solver.Add(solver.Sum(tmp) <= 1) # solver.Sum()은 리스트 안에 있는 모든 요소들을 더한다, worker가 2개의 task를 하지 못하는 제약

for j in range(num_tasks):
  tmp = []
  for i in range(num_workers):
    tmp.append(x[i,j])
  solver.Add(solver.Sum(tmp) == 1) # 하나의 과제는 한명의 worker가 한다는 제약식 
  
  
objective_terms = []
for i in range(num_workers):
  for j in range(num_tasks):
    objective_terms.append(costs[i][j]*x[i,j])
solver.Minimize(solver.Sum(objective_terms))


status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
  print("Total cost= ", solver.Objective().Value(), '\n')
  for i in range(num_workers):
    for j in range(num_tasks):
      if x[i,j].solution_value() > 0.5:
        print("Worker %d assigned to taks %d. Cost =%d" % (i,j,costs[i][j]))
