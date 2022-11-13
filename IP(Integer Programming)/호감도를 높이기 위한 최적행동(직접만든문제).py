# ------------------------------------- 그녀의 호감도를 최대로 높이기 위한 최적의 행동은? ------------------------------------ #
# 문제정의 
# A에게는 짝사랑하는 여자가 있다. 현재까지 경험상 특정 이모티콘을 보냈을 때 A에 대한 그녀의 호감도는 1회당 3상승, 그녀와 만나
# 밥을 먹으면 1회당 20000원이 소요되고 호감도는 10 상승, 카페를 가면 1회당 10000원이 소요되고 호감도는 5상승, 한강 자전거를 
# 타면 1회당 2000원이 소요되고 호감도는 5상승, 집에 데려다주면 5000원이 소요되고 호감도는 15만큼 상승 하였다.
# 과도한 이모티콘 사용은 오히려 그녀에게 부담이므로 하루 최대 5번, 시간 간격 1시간을 고려하여 1회 이모티콘을 보낼때마다 1시간이 걸리게 된다.
# 밥은 아침, 점심, 저녁을 고려해 최대 3번 먹을 수 있으며 1회당 2시간이 걸린다.
# 카페는 밥을 먹은 이후를 가기 때문에 최대 3번 갈 수 있으며 1회당 1시간이 걸린다. 
# 자전거는 계속 탈 수 있으며 1회당 1시간이 걸린다.
# 그녀의 집에 데려다 주는 건 1번만 가능하며 교통비 5000원과 2시간이 걸린다
# A는 그녀에게 하루에 7만원까지 쓸 수 있으며 자는 시간과 자잘한 이동시간을 제외한 16시간을 그녀에게 사용할 수 있다.

# 결정변수 

# x1 : 하루동안 그녀에게 이모티콘 보낸 횟수
# x2 : 하루동안 그녀와 밥을 먹은 횟수
# x3 : 하루동안 그녀와 카페를 간 횟수
# x4 : 하루동안 그녀와 자전거를 탄 횟수 
# x5 : 그녀의 집에 데려다준 횟수 

# 제약식 

# x1 + 2*x2 + x3 + x4 + 2*x5 <= 16
# 20000*x2 + 10000*x3 + 2000*x4 + 5000*x5 <= 70000
# x1 <= 5, x2 <= 3, x3 <= 3, x4 <= infinity, x5 <= 1
# x1 >= 0, x2 >= 0, x3 >= 0, x4 >= 0, x5 >= 0 

# 목적함수 

# max Z = 3*x1 + 10*x2 + 5*x3 + 5*x4 + 15*x5

!pip install ortools
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP') # SCIP solver는 integer programming 때 사용, GLOP은 LP일 때 사용

actives = [
    'emoticon',
    'restaurant',
    'cafe',
    'bicycle',
    'home',
          ]

infy = solver.infinity()
x = [solver.IntVar(0,infy,active) for active in actives]


solver.Add(x[0]+2*x[1]+x[2]+x[3]+2*x[4] <= 16)
solver.Add(20000*x[1]+10000*x[2]+2000*x[3]+5000*x[4] <= 70000)
solver.Add(x[0]<=5)
solver.Add(x[1]<=3)
solver.Add(x[2]<=3)
solver.Add(x[4]<=1)

solver.Maximize(3*x[0]+10*x[1]+5*x[2]+5*x[3]+15*x[4])

status = solver.Solve()
print(pywraplp.Solver.OPTIMAL)
if status == pywraplp.Solver.OPTIMAL:
  print("Solution:")
  print("Objective vaule = ", solver.Objective().Value())
  for i in range(len(x)):
    print(f"x{i+1} =", x[i].solution_value())
else:
  print("The problem does not have an optimal solution")
