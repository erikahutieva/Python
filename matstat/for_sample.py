import numpy as np
from scipy.stats import *
from scipy.stats import ks_2samp
from scipy.stats import anderson
import scipy.stats
from scipy.stats import wilcoxon
import numpy as np
from scipy.stats import chi2_contingency
from outliers import smirnov_grubbs as grubbs
import numpy as np
from scipy import stats
import math
from scipy.stats import kstest
from scipy.stats import ranksums
import json
from scipy.stats import median_test

# Сгенерируем случайные выборки
sample1 = np.random.normal(loc=4, scale=0.3, size=20)
sample2 = np.random.normal(loc=4, scale=0.22, size=10)
sample3=np.random.normal(loc=4, scale=0.2, size=10)

#with open('samples.txt', 'w') as file:
    # Записываем массивы
    #file.write('[' + ', '.join(map(str, sample1)) + ']\n')
    #file.write(' [' + ', '.join(map(str, sample2)) + ']\n')
    #file.write(' [' + ', '.join(map(str, sample2)) + ']\n')
#with open('samples.txt', 'r') as file:
    #sample1 = json.loads(file.readline())
    #sample2 = json.loads(file.readline())
    #sample3 = json.loads(file.readline())

#Критерий Грабса
def grubs_test(sample1):
    print('Критерий Грабса')
    n = len(sample1)  # Объем выборки
    mean = np.mean(sample1)  # Среднее значение
    std = np.std(sample1)  # Стандартное отклонение

    # Вычисляем критическое значение
    critical = t.ppf(1 - 0.05 / (2 * n), n - 2) 

    # Вычисляем критерий Грабса
    max_otkl = np.max(np.abs(sample1 - mean))  # Максимальное отклонение
    g = max_otkl / std  # Считаем значение критерия Граббса
    print("Критерий Грабса:", g)
    print("Критическое значение:", max_otkl) 

    # Проверяем гипотезу: если значение критерия Граббса меньше критического значения, то гипотезу принимают, иначе - не принимают.
    if g < max_otkl:
        print("Гипотезу принимают")
    else:
        print("Гипотезу не принимают")

    alpha = 0.05  # Уровень значимости
    dvustor_g = grubbs.test(sample1, 0.05)  # Двусторонний критерий Граббса

    mini = grubbs.min_test(sample1, alpha)  # Односторонний критерий Граббса для минимального значения
    maxi = grubbs.max_test(sample1, alpha)  # Односторонний критерий Граббса для максимального значения

    # Определяем индексы и значения аномальных наблюдений
    index = grubbs.two_sided_test_indices(sample1, alpha)
    anom = grubbs.two_sided_test_outliers(sample1, alpha)
    print("Индексы отклоняющихся чисел: ", index)


#Критерий Фишера
def fishsher(sample1,sample2,sample3):
    print('Критерий Фишера')

    # Выполнение однофакторного дисперсионного анализа
    F, p_value = f_oneway(sample1, sample2, sample3)
   
    # Объединение выборок в одну
    vib = np.concatenate([sample1, sample2, sample3])
   
    # Вычисление выборочного общего среднего
    sr = np.mean(vib)
   
    # Вывод результатов
    print("Выборочное общее среднее, a: ", sr)
    print("F: ", F)
    print("p_value: ", p_value)

#Критерий Стьюдента
def st(sample1,sample2 ):
    print('Критерий Стьюдента')
    n1=len(sample1)
    n2=len(sample2)
    # Вычисляем дисперсию и выборочные средние
    var1 = np.var(sample1, ddof=1)
    var2 = np.var(sample2, ddof=1)
    mean1 = np.mean(sample1)
    mean2 = np.mean(sample2)
    # Определяем какая выборка имеет большую дисперсию
    if var1>var2:
       sx=var1
       sy=var2
       nx=n1
       ny=n2
    else:
       sx=var2
       sy=var1
       nx=n2
       ny=n1
   
   # Вычисляем дисперсионное отношение
    f_stat = sx/ sy

    # Вычисляем p_value
    p_value = stats.f.sf(f_stat, nx-1, ny-1)

    # Определяем критическое значение дисперсионного отношения
    alpha = 0.05 #-точность
    crit_value = stats.f.ppf(1-alpha, nx-1, ny-1)
    #Сравниваем с критическим значением дисперсионного отношения
    if f_stat <= crit_value:
        print("Принимают")
        flag=0
    else:
        print("Отвергают")
        flag=1
    print("Дисперсия выборки 1:", var1)
    print("Дисперсия выборки 2:", var2)
    print("Дисперсионное отношение:", f_stat)
    print("p_value ",p_value)
    print("Критическое значение дисперсионного отношения:", crit_value)
    # Находим статистику t
    f1=n1-1 #Число степеней свободы
    f2=n2-1
    if flag==0 :
        f=f1+f2
        skv= (f1 * var1 + (f2) * var2) / (f) 
        t =abs( (mean1 - mean2) / math.sqrt(skv* (1/n1 + 1/n2)))#находим статистику
        
    else:
        t = abs((mean1 - mean2) / math.sqrt((var1/n1 + var2/n2)))
        c= (var1/n1)/(var1/n1+var2/n2)
        f=1/(c**2/f1+(1-c**2)/f2)
    # Находим критическое значение для уровня значимости альфа
    t_alpha=stats.t.ppf(1-alpha/2,f)
    print("Cтатистика",t)
    print("Критическое для уровня значимости альфа", t_alpha)
    # Сравниваем со статистикой t
    if t<t_alpha:
        print("Принимается")
    else:
        print("Отвергается")

#Критерий Бартлетта. Используется для проведения Бартлетта теста на равенство дисперсий в выборках.
#Тест Бартлетта проверяет нулевую гипотезу, что все выбранные выборки исходят из популяций с однаковыми дисперсиями. Если p-значение, #возвращаемое тестом, меньше 0,05 дисперсии выборок являются статистически различными.
def bartlett_test(sample1,sample2):
   # Вычисляем критерий Бартлетта
   bartle, p_value = stats.bartlett(sample1,sample2)
   print("Статистика теста:", bartle)
   print("p-значение:", p_value)

# Критерий Шапиро-Уилка.Тест Шапиро-Уилка используется для оценки нормальности распределения данных. Он помогает определить, насколько #хорошо данные подчиняются нормальному распределению.
def shapiro_test(sample1):
    print('Критерий Шапиро-Уилка')
    # Применение критерия Шапиро-Уилка
    stat, p = shapiro(sample1)
    
    # Вывод результатов
    print('Статистика критерия Шапиро-Уилка :', stat)
    print('p-значение критерия Шапиро-Уилка :', p)
    alpha = 0.05
    if p > alpha:
        print('Принимаем гипотезу: данные распределены нормально')
    else:
        print('Отвергаем гипотезу: данные не распределены нормально')

# Критерий Смирнова определяет соответсвует ли выборка нормальному распределению
def smirnov_test(sample1):
    print('Критерий Колмогорова-Смирнова')
    statistic, p_value = kstest(sample1, 'norm')
    print('statistic:', statistic)
    print('p-value:', p_value)

# Kритерий Андерсона-Дарлинга определяет соответсвует ли выборка нормальному распределению
def anderson_test(sample1):
    print('Kритерий Андерсона-Дарлинга')
    result = anderson(sample1, 'norm')
    print('Статистика критерия Андерсона-Дарлинга :', result.statistic)
    print('Критические значения:', result.critical_values)
    print('Уровни значимости:', result.significance_level)

# Критерий хи-квадрат позволяет проверить, есть ли значимая связь между sample1, sample2
def hi2(sample1,sample2):
    print('Критерий хи-квадрат')
    sample3=list(sample1)+list(sample2)
    chi2, p,f,b = chi2_contingency(sample3)
    print("Статистика хи-квадрат:", chi2)
    print("p-значение критерия хи-квадрат :", p)

#Критерий знаков для медианы позволяет проверить гипотезу о том, что медианы двух или более выборок равны
def medi(sample1, sample2):
    print('Критерий знаков для медианы')
    stat,p, med,f=scipy.stats.median_test(sample1, sample2)
    print("Статистика критерия знаков для медианы:", stat)
    print("p-значение критерия знаков для медианы:", p)
    print('Meдиана ', med )

#Критерий знаковых рангов Уилкоксона позволяет проверить гипотезу о том, что две независимые выборки имеют одинаковые распределения
def wilcoxon_test(sample1, sample2):
    print('Критерий знаковых рангов Уилкоксона')
    sample1 = np.array(sample1)
    sample2 = np.array(sample2)
    st, p = ranksums(sample1, sample2)
    print('Статистика критерия Уилкоксона:', st)
    print('p-value:', p)

#Критерий Колмогорова-Смирнова позволяет проверить, соответствуют ли два набора данных одному и тому же распределению.
def kolmogorov_smirnov_test(sample1, sample2):
    print('Критерий Колмогорова-Смирнова')
    p_value, statistic = ks_2samp(sample1, sample2)
    print('statistic',statistic)
    print('p_value', p_value)

#Критерий Краскела-Уоллиса проверяется гипотеза о равенстве распределений выборок
def kraskel_yollis(sample1,sample2):
   print('Критерий Краскела-Уоллиса')
   h_stat, p_val = stats.kruskal(sample1,sample2)
   print("Статистика Краскела-Уоллиса:", h_stat)
   print("p-значение:", p_val)

grubs_test(sample1)
fishsher(sample1,sample2,sample3)
st(sample1,sample2 )
bartlett_test(sample1,sample2)
shapiro_test(sample1)
smirnov_test(sample1)
anderson_test(sample1)
hi2(sample1,sample2)
medi(sample1, sample2)
wilcoxon_test(sample1, sample2)
kolmogorov_smirnov_test(sample1, sample2)
kraskel_yollis(sample1,sample2)
