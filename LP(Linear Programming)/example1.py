!pip install ortools
from ortools.linear_solver import pywraplp # OR library 호출


# 결정변수 정의
x = solver.NumVar(0, solver.infinity(), 'Study time for programming techniques') 
y = solver.NumVar(0, solver.infinity(), 'Study time for optimization problems')
print('Number of variables = ',solver.NumVariables())


# 제약조건 정의
#solver.Add(x <= 1)
#solver.Add(y <= 2)
#solver.Add(x+y <= 2)
#print('Number of constraints = ', solver.NumConstraints())

ct1 = solver.Constraint(-solver.infinity(),1) # -infinity <= x <= 1 
ct1.SetCoefficient(x, 1) # x변수의 계수 설정

ct2 = solver.Constraint(-solver.infinity() , 2 )
ct2.SetCoefficient(y,1)

ct3 = solver.Constraint(-solver.infinity(), 2)
ct3.SetCoefficient(x,1)
ct3.SetCoefficient(y,1) # -infinity <= x+y <= 2 
print('Number of constraints = ',solver.NumConstraints())

# 목적함수 정의 
# solver.Maximize(3*x + y)
obj = solver.Objective()
obj.SetCoefficient(x, 3)
obj.SetCoefficient(y, 1)
obj.SetMaximization() # 목적함수를 최대화 

# LP 문제 풀이 
status = solver.Solve()
print(pywraplp.Solver.OPTIMAL)
if status == pywraplp.Solver.OPTIMAL:
  print("Solution:")
  print("Objective vaule = ", solver.Objective().Value())
  print("x =", x.solution_value())
  print("y =", y.solution_value())
else:
  print("The problem does not have an optimal solution")

