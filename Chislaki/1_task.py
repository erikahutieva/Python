from math import *

def y(x):
    return sin(x+pi/3)-0.5*x

a=float(input("Введите число а "))
b=float(input("Введите число b "))
e=float(input("Введите точность "))

while y(a)*y(b)>=0:
    print("Функция не меняет знак")
    a=float(input("Введите число а "))
    b=float(input("Введите число b "))
    e=float(input("Введите точность "))

count=0

while b-a>=e:
    count+=1
    c=(a+b)/2
    if y(c) == 0:
        print(f'c = {c}, f(c) = {y(c)} = {y(c)}')
    else:
        print(f'Итерация {count}: a = {a}, b = {b}, c = {c}, f(c) = {y(c)}')
        if y(c)*y(a)<0:
            b=c
        else:
            a=c

print(f'Найденное значение c = {c}')
