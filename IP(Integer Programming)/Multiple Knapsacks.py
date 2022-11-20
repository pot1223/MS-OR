#Multiple Knapsacks
!pip install ortools
from ortools.linear_solver import pywraplp

#data
weights = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
values = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
bin_capacities =[100, 100, 100, 100, 100]
num_items = len(weights)
num_bins = len(bin_capacities)

#Definition solver
solver = pywraplp.Solver("Multiple Knapsacks", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)

#Decision valuable
x = {}
for i in range(num_items):
  for j in range(num_bins):
    x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i,j))

# constraints
for i in range(len(weights)):
  solver.Add(solver.Sum([x[i, j] for j in range(num_bins)]) <= 1)

for j in range(num_bins):
  solver.Add(solver.Sum([x[(i, j)] * weights[i] for i in range(len(weights))]) <= bin_capacities[j])

# Objective function
objective = solver.Objective()
for i in range(len(weights)):
  for j in range(num_bins):
    objective.SetCoefficient(x[(i, j)], values[i])
objective.SetMaximization()

# run
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
  print("Total packed value:" , objective.Value())
  total_weight = 0
  for j in range(num_bins):
    bin_weight = 0 
    bin_value = 0
    print('Bin ', j, '\n')
    for i in range(len(weights)):
      if x[i, j].solution_value() > 0:
        print('Item', i , '- weight:',weights[i], ' value:', values[i])
        bin_weight += weights[i]
        bin_value += values[i]
    print("Packed bin weight:", bin_weight)
    print("Packed bin value:", bin_value)
    print()
    total_weight += bin_weight
    print("Total packed weight:", total_weight)
else:
  print("The problem does not have an optimal solution.")
