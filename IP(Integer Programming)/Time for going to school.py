!pip install ortools
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver("Time for going to school",pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)

# data
arrival =[1,2,3,4,5,6,7,8]
depart = [1,2,3,4,5,6,7,8]
cost=[
    [1000000000, 35, 30, 25, 1000000000, 1000000000, 1000000000, 1000000000], # 독산역 출발지
    [1000000000, 1000000000, 3, 1000000000, 15, 1000000000, 1000000000, 1000000000],
    [1000000000, 5, 1000000000, 1000000000, 10, 1000000000, 1000000000, 1000000000],
    [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 35, 1000000000, 1000000000],
    [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 19, 15, 1000000000],
    [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 19, 7],
    [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 15, 1000000000, 10],
    [1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000, 1000000000], # 경기대 제 2공학관 도착지 
    ]

# decision variable 
x = {}
for i in arrival:
  for j in depart:
    x[i, j] = solver.IntVar(0, 1,'')
    
# constraint
solver.Add((solver.Sum(x[1,j] for j in depart) - solver.Sum(x[i,1] for i in arrival)) == 1 ) # 출발지 조건 (유출량 - 유입량 = 1)

for k in range(2,8):
  solver.Add((solver.Sum(x[k, j] for j in depart) - solver.Sum(x[i, k] for i in arrival)) == 0) # 경유지 조건 (유출량 - 유입량 = 0)

solver.Add((solver.Sum(x[8,j] for j in depart) - solver.Sum(x[i,8] for i in arrival)) == -1 ) # 도착지 조건 (유출량 - 유입량 = -1)

solver.Add(solver.Sum(x[i,6] for i in arrival) == 1) # 6번 도착지는 무조건 들려야 한다 
solver.Add(solver.Sum(x[i,7] for i in arrival) == 1) # 7번 도착지는 무조건 들려야 한다 

# objective function
objective_terms= []
for i in arrival:
  for j in depart:
    objective_terms.append(cost[i-1][j-1]*x[i,j]) 
solver.Minimize(solver.Sum(objective_terms))

# run
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
  print("Total time= ", solver.Objective().Value(),"분")
  for i in arrival:
    for j in depart:
      if x[i,j].solution_value() > 0:
        print("arrival %d assigned to depart %d. time = %d분" % (i, j , cost[i-1][j-1]))
else:
  print("No solution found.")
