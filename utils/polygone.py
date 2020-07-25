"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""


class Polygone(object):

    def __init__(self, render, vertices):
        self.render = render
        self.vertices = vertices

    def draw_polygone(self):
        for vertex in range(0, len(self.vertices)):
            x0 = self.vertices[vertex][0]
            y0 = self.vertices[vertex][1]

            x1 = self.vertices[vertex + 1][0] if vertex + 1 < len(self.vertices) else self.vertices[0][0]
            y1 = self.vertices[vertex + 1][1] if vertex + 1 < len(self.vertices) else self.vertices[0][1]

            self.render.glLine_coords(x0, y0, x1, y1)

    def has(self, x, y):
        j = len(self.vertices) - 1
        is_in = False
        for i in range(len(self.vertices)):
            x0 = self.vertices[i][0]
            y0 = self.vertices[i][1]
            x1 = self.vertices[j][0]
            y1 = self.vertices[j][1]
            if ((y0 > y) != (y1 > y)) and (x < x0 + (x1 - x0) * (y - y0) / (y1 - y0)):
                is_in = not is_in
            j = i
        return is_in
