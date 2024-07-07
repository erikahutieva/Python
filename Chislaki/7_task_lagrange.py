import numpy as np
x = np.array([0,1, 3, 5])
y = np.array([11, 12, 13,11])
x_star = 1

def basis(x_star, x, i):
    L_i = 1
    for j in range( len(x) ) :
        if j != i:
            L_i *= (x_star - x[j]) / (x[i] - x[j])
    return L_i

def lagrange(x_star, x, y_points):
    n = len(x)
    L_x = 0
    for i in range(n):
        L_x += y_points[i] * basis(x_star, x, i) 
    return L_x
f_x_star = lagrange(x_star, x, y)
print(f_x_star)