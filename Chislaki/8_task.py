from math import *
def f(x):
    return (x+1)/ (2+log (1+x**2))
def simpsons_rule(a, b):
    h = (b - a) / 2
    result = f(a) + f(b)
    for i in range(1, 2):
        if i%2==0 :
            result += 2 * f(a + 1 * h)
        else:
            result += 4 * f(a + 1 * h)
    result *= h / 3
    return result
def epsilon(a, b, e):
    n = 2
    integral_prev = 0
    integral_curr = simpsons_rule(a, b)
    while abs(integral_curr - integral_prev) > e:
        n*=2
        integral_prev = integral_curr
        integral_curr = simpsons_rule(a, b)
    return integral_curr
a=0
b=1
e =0.01
result = epsilon(a, b,e)
print ("Результат вычисления определенного интеграла:", result)