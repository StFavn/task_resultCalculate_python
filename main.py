import json
from collections import defaultdict
from datetime import datetime, timedelta
from time import time

def load_prizes(file_path):
    prizes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            prize = ' '.join(line.strip().split(' ')[2:])
            prizes.append(prize)
    return prizes

def calculate_time_delta(start, finish):
    time_format = '%H:%M:%S'
    start_time = datetime.strptime(start, time_format)
    finish_time = datetime.strptime(finish, time_format)

    if finish_time < start_time:
        finish_time += timedelta(days=1)

    delta = finish_time - start_time
    return str(delta)

def main():
    prize_files = {
        'M15': 'data/prizes_list_m15.txt',
        'M16': 'data/prizes_list_m16.txt',
        'M18': 'data/prizes_list_m18.txt',
        'W15': 'data/prizes_list_w15.txt',
        'W16': 'data/prizes_list_w16.txt',
        'W18': 'data/prizes_list_w18.txt'
    }
    
    prizes = {
        category: load_prizes(file_path) for category, file_path \
            in prize_files.items()
        }

    # Загрузка данных в память
    with open('data/race_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Форматирование данных и распределение по категориям
    categories = defaultdict(list)
    for entry in data:
        entry['Время'] = calculate_time_delta(
            entry['Время старта'], entry['Время финиша'])
        entry['Имя и Фамилия'] = f"{entry['Имя']} {entry['Фамилия']}"
        del entry['Имя']
        del entry['Фамилия']
        del entry['Время старта']
        del entry['Время финиша']
        categories[entry['Категория']].append(entry)
    
    # Сортировка и выдача призов для каждой категории  
    for category, items in categories.items():
        items.sort(key=lambda x: (x['Время'], x['Нагрудный номер']))
        category_prizes = prizes.get(category, [])
        for index, item in enumerate(items):
            item['Место'] = index + 1
            if index < 49:
                item['Приз'] = category_prizes[index]
            del item['Категория']

    # Запись данных в JSON файлы
    for category, items in categories.items():
        with open(f'{category}.json', 'w', encoding='utf-8') as file:
            json.dump(items, file, ensure_ascii=False, indent=4)
    
if __name__ == '__main__':
    main()
