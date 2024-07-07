def divided_diff(x, y):
    n = len(y)
    coef = [0] * n
    coef [0] = y[0]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            y[i] = (y[i] - y[i - 1]) / (x[i] - x[i - j])
        coef[j] = y[j]
    return coef
def newton_interpolation(x, y, x_val):
    coef = divided_diff(x, y.copy())
    n = len(coef)
    result = coef [0]
    for i in range(1, n):
        term = coef [i]
        for j in range(i):
            term *= (x_val - x[j])
        result += term
    return result
x = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
y= [1.2, 1.8, 3.2, 4.1, 5.2, 6.1]
x_vals = [1.1, 2.1]
results = {x_val: newton_interpolation(x, y, x_val) for x_val in x_vals}
for x_val, result in results.items():
    print(f"f({x_val}) = {result:.4f}")