from itertools import chain

import json
from parse import parse_vuzoteka


def write():
    with open("universities.json", "a") as f:
        f.write(json.dumps(parse_vuzoteka()))

def load():
    with open("universities.json", "r") as f:
        return json.loads(f.readline())



city = "Брянск"
for i in load():
    for j in i:
        if type(j) == dict and city.lower() in j["city"].lower():
            print(f"Name: {j['name']}\tStudents: {j['students']}\tRank: {j['rank']}")
