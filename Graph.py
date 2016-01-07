import networkx as nx
import matplotlib.pyplot as plt

#https://www.packtpub.com/books/content/visualizing-my-social-graph-d3js


# Load URL MAP
with open('./url_map.csv') as file:
    url_map = [x.split(";") for x in file.readlines() if len(x.split(";")) == 2]

# Load URL Relations
with open('./url_relations.csv') as file:
    url_relations = [x.split(";") for x in file.readlines() if len(x.split(";")) == 2]



start_limit = 49271
end_limit = len(url_map)

current = start_limit

while current < end_limit:
    print("{0} of {1} | {2}%".format(current, end_limit, (current / end_limit) * 100.0))

    # New Graph
    G = nx.Graph()

    # Get N elements from url_map
    sub_url_map = url_map[:current-1]

    for node in sub_url_map:
        G.add_node(node[1].replace("\n",""))

    nodes = G.nodes()

    for item in url_relations:
        n1 = item[0]
        n2 = item[1].replace("\n", "")

        if n1 in nodes and n2 in nodes:
            G.add_edge(n1, n2)

    Gcc = sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]

    pos=nx.spring_layout(Gcc)
    plt.axis('off')

    nx.draw_networkx_nodes(Gcc,pos,node_size=10)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

    figure = plt.gcf() # get current figure
    figure.set_size_inches(32, 24)

    plt.savefig("./Images/out_" + str(current) + ".png") # save as png

    current += 1