!pip install ortools
from ortools.linear_solver import pywraplp

#solver = pywraplp.Solver.CreateSolver('GLOP')
solver = pywraplp.Solver("A vitamin diet problem",pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# 사용되는 데이터 
vitamin_list = [
    ['Vitamin A (100IU)' ,50],
    ['Vitamin C (mg)', 60],
]
food_list = [
    ['Food 1',10,0,350],
    ['Food 2',0,10,300],
    ['Food 3',20,30,500],
    ['Food 4',20,10,340],
    ['Food 5',10,30,270],
    ['Food 6',20,20,400],
]

# 결정변수 정의
x = [solver.NumVar(0.0,solver.infinity(),food[0]) for food in food_list]
print("Number of variables =", solver.NumVariables())

# 제약조건 정의 
# CT1 : 50 <= 10*x1 + 0*x2 + 20*x3 + 20*x4 + 10*x5 + 20*x6 <= infinity
# CT2 : 60 <= 0*x1 + 10*x2 + 30*x3 + 10*x4+ 30*x5 + 20*x6 <= infinity
constraints = [] 
for i, vitamin in enumerate(vitamin_list):
  constraints.append(solver.Constraint(vitamin[1],solver.infinity()))
  for j, food in enumerate(food_list):
    constraints[i].SetCoefficient(x[j],food[i+1])
print("Number of constraints =", solver.NumConstraints())

# 목적함수 정의
# Min 350 * x1 + 300 * x2 + 500 * x3 + 340 * x4 + 270 * x5 + 400 * x6
obj = solver.Objective()
for k , food in enumerate(food_list):
  obj.SetCoefficient(x[k],food[3])
obj.SetMinimization() # 목적함수를 최소화 

# LP 문제 풀이 
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
  for j in range(0,len(food_list)):
    print(f"The purchase amount of food {j+1} =",x[j].solution_value())
else:
  print("The problem does not have an optimal solution")

print("\nAdvanced usage:")
print("Problem solved in ",solver.wall_time(),' milliseconds')
print("Problem solved in ", solver.iterations(),' iterations')
