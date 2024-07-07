import numpy as np

def find_znach(A, num_iterations):
    n=3
    x = np.array([1,1,1])
    for _ in range(num_iterations):
        x = A. dot(x)
        x = x / (x[0]**2+x[1]**2+x [2]**2)
    sobstv_znach = np.dot (A.dot(x), x) / np.dot (x, x)
    return sobstv_znach
A = np.array([[1, 2, -7],
            [2, 3, 4],
            [-7, 4, 5]])
iterations = 1000
sobstv_znach = find_znach(A, iterations)
print ("Собственное значение:", sobstv_znach)