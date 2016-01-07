__author__ = 'PerArne'
import json

themap = []
with open('url_map.csv') as file:
    for item in file.readlines():

        split = item.split(";")

        if len(split) !=  2:
            continue

        url = split[0]
        _id = split[1].replace("\n", "")

        themap.append([url, _id])

with open('url_map.json', "w") as file:
    file.write(json.dumps(themap, sort_keys=True))


thelist = []
with open('url_relations.csv') as file:
    for item in file.readlines():

        split = item.split(";")

        if len(split) != 2:
            continue

        rel1 = split[0]
        rel2 = split[1].replace("\n", "")

        thelist.append([rel1,rel2])

with open('url_relations.json', "w") as file:
    file.write(json.dumps(thelist))
