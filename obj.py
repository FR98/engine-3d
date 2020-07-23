"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""


class Obj(object):

    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()
        
        self.vertices = []
        self.normals = []
        self.texture_coords = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            if len(line) > 0:
                prefix, value = line.split(' ', 1)
                
                if prefix == 'v':
                    # x, y, z
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    # x, y, z
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':
                    self.texture_coords.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    # f = v/vt/vn
                    self.faces.append([list(map(int, vertex.split('/'))) for vertex in value.split(' ')])
