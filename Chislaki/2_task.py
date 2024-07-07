def newton(f, df, x0):
    e=8.001
    iter=100
    x_n = float (x0)
    for i in range(iter): 
        f_x_n= f(x_n)
        df_x_n = df (x_n)
        x_next = x_n - f_x_n / df_x_n
        if abs (x_next - x_n) < e:
            return x_next
        x_n = x_next
    return "Решение не сходится."
def hord(f, x0, x1, e=0.001, iter=100):
    f_x0 = f(x0)
    f_x1 = f(x1)
    for n in range(iter):
        x_next = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        if abs(x_next - x1) < e:
            return float (x_next)
        xO, x1 = x1, x_next
        f_x0, f_x1 = f_x1, f(x_next)
    return float (x1)
f = lambda x: x**3 + 3*x-1
df = lambda x: 3*x**2 + 3
print ("Метод Ньютона:", newton(f, df, x0=1.0))
print ("Метол хорд:", hord(f, x0=1.0, x1=2.0))