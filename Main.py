import Filehandler
import Worker
import json
from tld import get_tld

# Load existing data
data, counter, blacklist = Filehandler.load()


def write_to_disk():

    tmp = data.copy()
    tmp['edges'] = list(tmp['edges'])

    with open("./Processor/data.json", 'w') as file:
        file.write(json.dumps(tmp))



def add_visited(url):
    with open("url_visited.csv", 'a') as file:
        file.write(url + "\n")

def add_url(url):
    global counter

    try:
        res = get_tld(str(url), as_object=True)
        domain = res.domain
    except:
        domain = url

    # Create new entry for this domain
    if domain not in data['nodes']:
        data['nodes'][domain] = {
            'id': counter,
            'domains': [],
            'size': 0
        }

        counter += 1

    data['nodes'][domain]['domains'].append(url)
    data['nodes'][domain]['size'] = len(data['nodes'][domain]['domains'])
    return data['nodes'][domain]['id']


def add_relations(node_1_id, node_2_ids):
    for edge in [';'.join(sorted([str(node_1_id), str(node_2_id)])) for node_2_id in node_2_ids]:
        data['edges'].add(edge)



"""
def add_new_urls(new_urls):
    for new_url in new_urls:
        hash2 = add_url(new_url['url'])

        # Add relation
        add_relations(hash1,  hash2)

    if len(new_urls) == 0:
        print("NO new")



#############################################
#
# Variable Definitions
#
############################################
queue = [Filehandler.getpage()]
max_threads = 16


#############################################
#
# Future Processing
#
############################################
futures = []
def process_futures():
    while True:
        for future in futures:
            if future.done():
                # Fetch new urls from the resulting thread
                new_urls = future.result()

                # Add new urls to maps
                add_new_urls(new_urls)

                # Add new urls to queue
                for new_url in new_urls:
                    if new_url['url'] in blacklist:
                        continue
                    queue.append(new_url)

                # Remove completed future
                futures.remove(future)

        time.sleep(.5)
t = threading.Thread(target=process_futures)
t.daemon = True
t.start()

#############################################
#
# Handler Configuration
#
############################################
handler = Handler.Handler(max_threads)


#############################################
#
# Handler Queue Handler
#
############################################
empty_queue_tick = 0
while True:

    # Skip tick, if futures queue is full
    if len(futures) >= max_threads:
        time.sleep(1)
        continue

    # If no items in queue, increment empty queue tick
    if len(queue) == 0:
        empty_queue_tick += 1
        time.sleep(.2)
        continue
    else:
        empty_queue_tick = 0

    # Get new page from dataset if no new item is added to queue for 50 ticks
    if empty_queue_tick > 50:
        queue.append(Filehandler.getpage())
        continue

    # Add future
    url = queue.pop()

    # Add to url_map if not already exists
    hash1 = add_url(url['url'])
    futures.append(handler.add(Worker.scrape, url, blacklist))
    add_visited(url['url'])

    #print("Status: q:" + str(len(queue)) + " | eqt:" + str(empty_queue_tick))
    time.sleep(.5)



"""






queue = Worker.scrape(Filehandler.getpage(), blacklist)
i = 0
while len(queue) > 0:

    # Fetch url from queue
    url = queue.pop()

    # Scrape the url, and retrieve new urls
    new_urls = Worker.scrape(url, blacklist)

    # Add new URL's to the queue
    queue.extend(new_urls)

    # Mark this url as visited
    add_visited(url['url'])

    # Add urls and retrieve hashes
    hash1 = add_url(url['url'])
    hash2s = [add_url(x['url']) for x in new_urls]

    # Add relations
    add_relations(hash1, hash2s)

    if i % 20 == 0:
        write_to_disk()
        print("Saving!")

    i += 1

    # If queue happens to be empty on this point...
    while len(queue) == 0:
        for i in Worker.scrape(Filehandler.getpage(), blacklist):
            queue.append(i)










print("Done! (Should never happen tho : > ")
