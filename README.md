# Парсер [Вузотеки](https://vuzoteka.ru/)

Парсер ВУЗов из сервиса [Вузотека](https://vuzoteka.ru/)


## Пример использования

```python
import json
from parse import parse_vuzoteka


with open("universities.json", "a") as f:
    f.write(json.dumps(parse_vuzoteka()))

with open("universities.json", "r") as f:
    load = json.loads(f.readline())


city = "Брянск"
for i in load:
    for j in i:
        if type(j) == dict and city.lower() in j["city"].lower():
            print(f"Name: {j['name']}\tStudents: {j['students']}\tRank: {j['rank']}")
```


## Функция load

Функция load возвращает список, в котором находятся списки(страницы вузотеки),
в которых находятся словари с ключами `rank`, `url`, `logo`, `name`, `city`,
`average ege`, `students`.
