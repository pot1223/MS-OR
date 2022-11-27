!pip install ortools
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver("chocolate",pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

machine = ['A' , 'B']
month =[5, 6, 7, 8, 9]
demand =[300, 400, 200, 300, 100]
price = [10, 50]

# decision variable 
x = {}
for i in machine:
  for j in month:
    x[i, j] = solver.NumVar(0, solver.infinity(),'')
    
# constraint
for j in month:
  if j+1 == 10:
    break;
  solver.Add(x['B',j+1] <=0.9 * x['B',j])

for j in month :
    solver.Add(x['A', j] + 10* x['B', j] >= demand[j-5])
    
# objective function
objective_terms= []
k = 0 
for i in machine:
  for j in month:
    objective_terms.append(price[k]*x[i,j])
  k += 1 
solver.Minimize(solver.Sum(objective_terms))

# run 
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
  print("Total cost= ", solver.Objective().Value(),"만원")
  for i in machine:
    for j in month:
      print(f"{j} machine {i} usage time(h) : {x[i,j].solution_value()}")
else:
  print("No solution found.")
