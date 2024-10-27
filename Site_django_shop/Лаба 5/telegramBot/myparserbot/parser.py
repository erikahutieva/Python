import requests
from bs4 import BeautifulSoup as bs

def get_prices(URL, headers):
    response = requests.get(URL, headers=headers)
    soup = bs(response.text, 'html.parser')

    trs = soup.find_all('tr')

    prices = []

    for tr in trs[1:]:
        tds = tr.find_all('td')
        price = round(float((tds[4].text).replace(',', '.'))/float(tds[2].text), 2)
        prices.append([tds[1].text, price])

    return prices

def resault_to_str(array):
    line = ''
    for a in array:
        line += a[0] + ' - ' + str(a[1]) + '₽' + '\n'
    return line

if __name__ == '__main__':
    URL = r"https://www.cbr.ru/currency_base/daily/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    print(get_prices(URL, headers=headers))