import numpy as np 
import matplotlib.pyplot as plt 
from math import *

def eiler(f, t0, y0, t_end, h):
    t_values = np.arange(t0, t_end + h, h)
    y_values = np.zeros( len(t_values))
    y_values [0] = y0
    for i in range(1, len(t_values)):
        y_values [i] = y_values [i-1] + h * f(t_values [i-1], y_values[i-1])
    return t_values, y_values 
def f(t, y):
    return cos((t*y**2) **(0.5))

t0 = 1
y0 = 2
T = 2
N = 0.1
t_values, y_values = eiler(f, t0, y0, T, N)
plt.plot(t_values, y_values, label="Метод Эйлера")
plt.xlabel('t')
plt.ylabel('y')
plt.legend()
plt.show()