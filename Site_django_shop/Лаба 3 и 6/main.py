import requests  # Импорт библиотеки для отправки HTTP-запросов
from bs4 import BeautifulSoup as bs  # Импорт функционала Beautiful Soup для парсинга HTML-страниц
import datetime  # Импорт модуля для работы с датой и временем

############################################################################################
def get_prices(URL, headers):  # Функция для получения курсов валют с сайта ЦБ РФ
    """
    Получает курсы валют с указанного URL.
    
    Аргументы:
        URL (str): Ссылка на страницу с курсами валют.
        headers (dict): Заголовки для HTTP-запроса.
        
    Возвращает:
        list: Список курсов валют.
    """
    response = requests.get(URL, headers=headers)  # Отправка GET-запроса
    soup = bs(response.text, 'html.parser')  # Создание объекта Beautiful Soup для парсинга HTML

    trs = soup.find_all('tr')  # Поиск всех элементов tr в HTML-коде

    prices = []  # Инициализация списка для хранения курсов валют

    for tr in trs[1:]:  # Перебор всех tr, начиная со второго
        tds = tr.find_all('td')  # Поиск всех элементов td в текущем tr
        # Расчет курса валюты и добавление его в список курсов
        price = round(float((tds[4].text).replace(',', '.')) / float(tds[2].text), 2)
        prices.append([tds[1].text, price])

    return prices  # Возвращение списка курсов валют

def resault_to_str(array):  # Функция для преобразования списка курсов в строку
    """
    Преобразует список курсов в строку.
    
    Аргументы:
        array (list): Список курсов валют.
        
    Возвращает:
        str: Строка с курсами валют.
    """
    line = ''  # Инициализация пустой строки
    for a in array:  # Перебор всех элементов списка курсов
        # Формирование строки с курсом валюты и добавление к строке line
        line += a[0] + ' - ' + str(a[1]) + '₽' + '\n'
    return line  # Возвращение строки с курсами

############################################################################################
def get_prices2(URL, headers):  # Функция для получения курсов валют с сайта myfin.by
    """
    Получает курсы валют с указанного URL.
    
    Аргументы:
        URL (str): Ссылка на страницу с курсами валют.
        headers (dict): Заголовки для HTTP-запроса.
    """
    banks = []  # Инициализация списка для хранения курсов валютных банков
    for i in range(1, 5):  # Цикл для обхода страниц с курсами валют
        response = requests.get(URL + f'{i}', headers=headers)  # Отправка GET-запроса
        soup = bs(response.text, 'html.parser')  # Создание объекта Beautiful Soup для парсинга HTML

        trs = soup.find_all('tr', class_='tr-turn')  # Поиск всех элементов tr с классом 'tr-turn'
        for tr in trs:  # Перебор всех tr
            tds = tr.find_all('td')  # Поиск всех элементов td в текущем tr
            # Добавление курсов валютного банка в список banks
            banks.append([tds[0].find('a').text, [tds[1].text, tds[2].text], [tds[3].text, tds[4].text]])
    
    for bank in banks:  # Перебор всех курсов валютных банков
        # Вывод информации о курсах валютного банка
        print(bank[0], f'- USD покупка: {bank[1][0]}, USD продажа: {bank[1][1]}, EUR покупка: {bank[2][0]}, EUR продажа: {bank[2][1]}')

    buyUSD = 0  # Инициализация переменной для суммы покупки USD
    sellUSD = 0  # Инициализация переменной для суммы продажи USD
    buyEUR = 0  # Инициализация переменной для суммы покупки EUR
    sellEUR = 0  # Инициализация переменной для суммы продажи EUR

    for bank in banks:  # Перебор всех курсов валютных банков
        # Расчет сумм покупки и продажи USD и EUR
        buyUSD += float(bank[1][0])
        sellUSD += float(bank[1][1])
        buyEUR += float(bank[2][0])
        sellEUR += float(bank[2][1])

    n = len(banks)  # Получение количества курсов валютных банков
    # Расчет средних значений покупки и продажи USD и EUR
    buyUSD /= n
    sellUSD /= n
    buyEUR /= n
    sellEUR /= n
    print('\nСреднии покупка USD, продажа USD, покупка EUR, продажа EUR')
    print(buyUSD, sellUSD, buyEUR, sellEUR)  # Вывод средних значений

if __name__ == '__main__':  # Проверка, что скрипт был запущен напрямую
    headers = {  # Заголовки для HTTP-запроса
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    print(f"Курсы валют от ЦБ РФ на {datetime.datetime.today().strftime('%d/%m/%Y %H:%M')}")  # Вывод даты и времени
    print(resault_to_str(get_prices("https://www.cbr.ru/currency_base/daily/", headers=headers)))  # Вывод курсов ЦБ РФ

    print('-----------------------------------------------------------------\n')

    get_prices2("https://ru.myfin.by/currency?page=", headers=headers)  # Получение и вывод курсов myfin.by
