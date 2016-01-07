__author__ = 'perar'
import math
import random

class Graph:

    EPSILON = 0.000001

    def __init__(self, nodes, edges, max_iterations = 1000, area=5000):
        self.attraction_multiplier = 5
        self.repulsion_multiplier = 0.75
        self.max_iterations = max_iterations
        self.width = 5000
        self.height = 5000

        self.area = area

        self.attraction_constant = None
        self.repulsion_constant = None
        self.force_constant = None

        self.layout_iterations = 0
        self.temperature = 0

        self.nodes = nodes
        self.edges = edges

        self.init()

    def init(self):
        self.temperature = self.width / 10.0
        self.force_constant = math.sqrt(self.height * self.width / len(self.nodes))
        self.attraction_constant = self.attraction_multiplier * self.force_constant
        self.repulsion_constant = self.repulsion_multiplier * self.force_constant

        # Generate random start position
        for node in self.nodes:
            node.o_x = (random.random() * (self.area + self.area + 1) - self.area)
            node.o_y = (random.random() * (self.area + self.area + 1) - self.area)
            node.o_z = (random.random() * (self.area + self.area + 1) - self.area)
            node.x = node.o_x
            node.y = node.o_y
            node.z = node.o_z


    def result(self):
        res = {
            'nodes': {},
            'edges': []
        }

        # Nodes
        for node in self.nodes:
            res['nodes'][node.id] = {
                'id': node.id,
                'size': node.size,
                'text': node.text,
                'position': {
                    'x': node.x,
                    'y': node.y,
                    'z': node.z
                }
            }

        for edge in self.edges:
            res['edges'].append([edge.node1.id, edge.node2.id])

        return res


    def generate(self):

        if not (self.layout_iterations < self.max_iterations and self.temperature > 0.000001):
            pass
        else:

            # Calculate Repulsion
            for i, node1 in enumerate(self.nodes):

                # First item
                if i == 0:
                    node1.offset_x = 0
                    node1.offset_y = 0
                    node1.offset_z = 0

                node1.force = 0

                node1.tmp_pos_x = node1.tmp_pos_x or node1.x
                node1.tmp_pos_y = node1.tmp_pos_y or node1.y
                node1.tmp_pos_z = node1.tmp_pos_z or node1.z

                for j, node2 in enumerate(self.nodes):
                    if i == j:
                        continue

                    if i != j:
                        node2.tmp_pos_x = node2.tmp_pos_x or node2.x
                        node2.tmp_pos_y = node2.tmp_pos_y or node2.y
                        node2.tmp_pos_z = node2.tmp_pos_z or node2.z

                    delta_x = node1.tmp_pos_x - node2.tmp_pos_x
                    delta_y = node1.tmp_pos_y - node2.tmp_pos_y
                    delta_z = node1.tmp_pos_z - node2.tmp_pos_z

                    delta_length = max(self.EPSILON, math.sqrt((delta_x * delta_x) + (delta_y * delta_y)))
                    delta_length_z = max(self.EPSILON, math.sqrt((delta_z * delta_z) + (delta_y * delta_y)))

                    force = (self.repulsion_constant * self.repulsion_constant) / delta_length
                    force_z = (self.repulsion_constant * self.repulsion_constant) / delta_length_z

                    node1.force += force
                    node2.force += force

                    if i == 0:
                        node2.offset_x = 0
                        node2.offset_y = 0
                        node2.offset_z = 0

                    node1.offset_x += (delta_x / delta_length) * force
                    node1.offset_y += (delta_y / delta_length) * force
                    node1.offset_z += (delta_y / delta_length) * force_z

                    node2.offset_x -= (delta_x / delta_length) * force
                    node2.offset_y -= (delta_y / delta_length) * force
                    node2.offset_z -= (delta_y / delta_length) * force_z

            # Calculate Attraction
            for edge in self.edges:

                delta_x = edge.node1.tmp_pos_x - edge.node2.tmp_pos_x
                delta_y = edge.node1.tmp_pos_y - edge.node2.tmp_pos_y
                delta_z = edge.node1.tmp_pos_z - edge.node2.tmp_pos_z

                delta_length = max(self.EPSILON, math.sqrt((delta_x * delta_x) + (delta_y * delta_y)))
                delta_length_z = max(self.EPSILON, math.sqrt((delta_z * delta_z) + (delta_y * delta_y)))

                force = (delta_length * delta_length) / self.attraction_constant
                force_z = (delta_length_z * delta_length_z) / self.attraction_constant

                edge.node1.force -= force
                edge.node2.force += force

                edge.node1.offset_x -= (delta_x / delta_length) * force
                edge.node1.offset_y -= (delta_y / delta_length) * force
                edge.node1.offset_z -= (delta_z / delta_length) * force_z

                edge.node2.offset_x -= (delta_x / delta_length) * force
                edge.node2.offset_y -= (delta_y / delta_length) * force
                edge.node2.offset_z -= (delta_z / delta_length) * force_z

            # Calculation Position
            for node in self.nodes:

                delta_length = max(self.EPSILON, math.sqrt(node.offset_x * node.offset_x + node.offset_y * node.offset_y))
                delta_length_z = max(self.EPSILON, math.sqrt(node.offset_z * node.offset_z + node.offset_y * node.offset_y))

                node.tmp_pos_x += (node.offset_x / delta_length) * min(delta_length, self.temperature)
                node.tmp_pos_y += (node.offset_y / delta_length) * min(delta_length, self.temperature)
                node.tmp_pos_z += (node.offset_z / delta_length_z) * min(delta_length_z, self.temperature)

                node.x -= (node.x - node.tmp_pos_x) / 10
                node.y -= (node.y - node.tmp_pos_y) / 10
                node.z -= (node.z - node.tmp_pos_z) / 10

                #print("{0},{1},{2}".format(str(node.x - node.o_x), str(node.y - node.o_y), str(node.z - node.o_z)))

            self.temperature *= (1 - (self.layout_iterations / self.max_iterations))
            self.layout_iterations += 1
