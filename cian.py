import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import pandas as pd
import matplotlib.pyplot as plt

def clean_price(price):
    """Очистка строки с ценой, удаление '₽/мес.' и пробелов, преобразование в число."""
    return int(price.replace(' ₽/мес.', '').replace(' ', ''))

# Настройка Firefox для работы в фоновом режиме (если необходимо)
options = Options()
options.add_argument('--headless')  # Добавляем аргумент для headless режима
options.add_argument('--disable-gpu')  # Отключаем GPU для headless режима
options.add_argument('--no-sandbox')  # Безопасный режим (используется в некоторых системах)

# Указываем путь к geckodriver (необходимо, если он не находится в PATH)
# service = Service(executable_path='/path/to/geckodriver')

# Инициализация драйвера Firefox
driver = webdriver.Firefox(options=options)  #, service=service)

try:
    # URL страницы для парсинга
    url = 'https://www.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/'

    # Открытие страницы
    driver.get(url)

    # Ждем некоторое время, чтобы страница полностью загрузилась
    time.sleep(5)

    # Парсинг цен
    prices = driver.find_elements(By.XPATH, "//span[@data-mark='MainPrice']/span")

    # Открытие CSV файла для записи
    with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Price'])  # Записываем заголовок столбца

        # Записываем цены в CSV файл
        for price in prices:
            writer.writerow([price.text])

finally:
    # Закрытие драйвера
    driver.quit()

# Чтение данных из исходного CSV файла и их обработка
input_file = 'prices.csv'
output_file = 'cleaned_prices.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Читаем заголовок и записываем его в новый файл
    header = next(reader)
    writer.writerow(header)

    # Обрабатываем и записываем данные строк
    for row in reader:
        clean_row = [clean_price(row[0])]
        writer.writerow(clean_row)

print(f"Обработанные данные сохранены в файл {output_file}")

# Загрузка данных из CSV-файла
data = pd.read_csv(output_file)

# Предположим, что столбец с ценами называется 'Price'
prices = data['Price']

# Построение гистограммы
plt.hist(prices, bins=10, edgecolor='black')

# Добавление заголовка и меток осей
plt.title('Гистограмма цен')
plt.xlabel('Цена')
plt.ylabel('Частота')

# Показать гистограмму
plt.show()
