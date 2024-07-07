import numpy as np

def F(x):
    return np.array([
        2*x [0]-np.cos (x [1]+1),
        np.sin(x[0]) + 2*x[1] + 0.4])

def J(x):
    return np.array([
    [2, np.sin(x[1]+1)],
    [np. cos(x[0]), 2]])

def newton_system(F, J, x0):
    x= np.array(x0, dtype=float)
    while True:
        delta_x = np.linalg.solve(J(x), -F(x))
        x = x + delta_x
        if np.linalg.norm(delta_x) < e:
            break
    return x
x0 = [0.0, 0.0]
e = 0.001
solution = newton_system(F, J, x0)
print ("Решение системы: ", solution)
