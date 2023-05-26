import numpy as np


def x2(x1):
    return (8.699 - 2.352 * np.log(x1) + 0.066 * x1 - 129.032)/ -(0.1594 + 0.2787 * np.log(x1) -0.003334 * x1)

def f(x1):
    return (100 - 4687.7 * pow(x2(x1), -1.002))/(413.2 * pow(x2(x1), -0.96)) - x1

def bisection_method():
    a = 15  # min guess for x1 
    b = 20  # max guess for x1
    tolerance = 1e-6  # Desired tolerance for convergence
    max_iterations = 1000  # Maximum number of iterations

    iteration = 0
    while abs(b - a) > tolerance and iteration < max_iterations:
        c = (a + b) / 2

        if f(a) * f(c) < 0:
            b = c
        elif f(b) * f(c) < 0:
            a = c
        else:
            break

        iteration += 1
    print("Iterations:", iteration)
    return c, x2(c)

result = bisection_method()
print("Solution: x1 =", result[0], "x2 =", result[1])