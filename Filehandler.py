import random
from urllib.parse import urlparse
import json

dataset_size = 1000000 # Dataset size


# Fetch a random web site
def getpage():

    offset = random.randrange(dataset_size)

    f = open('./Dataset/top-1m.csv')
    f.seek(offset)
    f.readline()
    random_page = f.readline()

    # Edge handling
    if len(random_page) == 0:
        f.seek(0)
        random_page = f.readline()

    return {
        'url': 'http://' + random_page.split(",")[1].replace("\n", ""),
        'n': 0
    }


def load():

    data = {
        'nodes': {},
        'edges': set()
    }
    counter = 0
    blacklist = []

    # Attempt to load url map
    try:
        with open("./Processor/data.json", 'r') as file:
            data = json.loads(file.read())
            data['edges'] = set(data['edges'])
            counter = len(data)
    except FileNotFoundError:
        pass

    #generate blacklist
    try:
        with open("url_visited.csv", 'r') as file:
            for line in file.readlines():
                blacklist.append(line.replace("\n", ""))
    except FileNotFoundError:
        pass

    print(blacklist)

    return data, counter, blacklist

