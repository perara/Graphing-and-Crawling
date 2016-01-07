__author__ = 'perar'
from Node import Node
from Edge import Edge
from Graph_SP import Graph
import json
import time

data = None

nodes = []
node_map = {}
edges = []

with open("./data.json", "r") as file:
    data = json.loads(file.read())


# Load nodes
for domain, node_data in data['nodes'].items():

    # Create node
    node = Node(node_data['id'], node_data['domains'][0], size = node_data['size'])

    # Add to list
    nodes.append(node)

    # Add to map
    node_map[node_data['id']] = node

# Load edges
for edge_data in data['edges']:
    split = edge_data.split(";")

    node_1 = node_map[int(split[0])]
    node_2 = node_map[int(split[1])]

    edge = Edge(node_1, node_2)

    edges.append(edge)


graph = Graph(nodes, edges)



if __name__ == "__main__":
    print("Starting Computations...")
    iterations = 1000
    estimate_tick_complete = 200
    total_time = 0
    for i in range(iterations):
        start = time.time()
        graph.generate()
        end = time.time() - start

        total_time += end

        print("{0}/{1} | Est: {2}m | Max: {3}m | Cur: {4}m".format(
            i,
            iterations,
            str(int((end * estimate_tick_complete) / 60)),
            str(int((end * iterations) / 60)),
            str(int((total_time / 60)))
        ))

    with open('../public_html/nodes.json', "w") as file:
        file.write(json.dumps(graph.result()))




