__author__ = 'perar'


class Node:

    def __init__(self, id, text, size=1):

        self.size = size

        self.o_x = None
        self.o_y = None
        self.o_z = None

        self.x = None
        self.y = None
        self.z = None

        self.tmp_pos_x = None
        self.tmp_pos_y = None
        self.tmp_pos_z = None

        self.offset_x = 0
        self.offset_y = 0
        self.offset_z = 0

        self.force = 0

        self.id = id
        self.text = text
