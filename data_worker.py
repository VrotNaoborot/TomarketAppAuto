import csv
from requests_data import login_api

DATA_FILE = 'data.csv'


def reader_data():
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        rows = list(reader)
        return rows


# def checkout_access():
#     """Проверка access, если отсутствует - получает и записывает."""
#     try:
#         print(f"Проверка access токенов")
#
#         with open(DATA_FILE, mode='r', encoding='utf-8') as file:
#             reader = csv.DictReader(file, delimiter=';')
#             rows = list(reader)
#
#         updated = False
#         print(rows)
#
#         for dct in rows:
#             if dct['access_token'] == '':
#                 dct['access_token'] = login_api(dct['query'])
#                 updated = True
#
#         if updated:
#             print("Записываем полученные токены")
#             with open(DATA_FILE, mode='w', encoding='utf-8', newline='') as file:
#                 writer = csv.DictWriter(file, fieldnames=reader.fieldnames, delimiter=';')
#                 writer.writeheader()
#                 writer.writerows(rows)
#
#     except KeyError:
#         print("Файл data.csv поврежден")
#     except FileNotFoundError:
#         print("Файл data.csv не существует")
#     except Exception as ex:
#         print(f"Неизвестная ошибка: {ex}")
