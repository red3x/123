import requests
import json
import random

address = 'http://127.0.0.1:1337/'
list_tasks = ['America/Port_of_Spain','America/Bogota','Europe/Vaduz','Australia/Canberra','Europe/Riga','Pacific/Easter','US/Hawaii',
              'Asia/Omsk','Asia/Tokyo','Etc/GMT-11','Cuba','Europe/Berlin','EST','Europe/Zaporozhye','Pacific/Kwajalein','Turkey','Singapore']
MAX = len(list_tasks) - 1

# TIME
print('\nВремя:\n')
for task in list_tasks:
    task_address = address + task
    response = requests.get(task_address)
    print(f'Текущее время в {task.split("/")[-1]}: {response.text}')

# CONVERTER
print('\nНачальная дата: 10.04.2076 03:40:11\n')
for i in range(6):
    rand = random.randrange(0, MAX, 1)
    task_conv = list_tasks[rand]
    task_address_conv = 'http://127.0.0.1:1337/api/v1/convert'
    task_data_conv = json.dumps(
        {"date": {"date": "10.04.2076 03:40:11",
               "tz": "EST"},
         "target_tz": task_conv }
    )

    response = requests.post(task_address_conv, json=task_data_conv)
    print(f'Преобразование часового пояса EST в {task_conv.split("/")[-1]}: {response.text}')

# DIFFERENCE
print('\nРазница в секундах:\n')
for i in range(6):
    rand = random.randrange(0, MAX, 1)
    task_diff = list_tasks[rand]
    task_address_diff = 'http://127.0.0.1:1337/api/v1/datediff'
    task_data_diff = json.dumps(
        {"first_date": "9.11.2001 00:05:29",
        "first_tz": "EST",
        "second_date": "9.11.2001 00:00:09",
        "second_tz": task_diff}
    )

    response = requests.post(task_address_diff, json=task_data_diff)
    print(f'Число секунд между EST и {task_diff.split("/")[-1]}: {response.text}')
