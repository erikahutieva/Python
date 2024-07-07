import math

def simple_iteration() :
    e=0.001
    x,y= 0, 0  # Начальные значения
    iteration_count = 0
    while True:
        x_new = math.cos(y - 1) / 2
        y_new = -0.4 - math.sin(x)
        if abs(x_new - x) < e and abs (y_new - y) < e:
            break
        x,y = x_new, y_new
        iteration_count += 1
    return x, y
x_solution, y_solution = simple_iteration()
print ("Решение: ")
print("x = ", x_solution)
print("y = ", y_solution)