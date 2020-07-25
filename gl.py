"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from utils.color import Color
from utils.memory import MemorySize
from utils.polygone import Polygone
from obj import Obj
import utils.glmath as glmath


class Render(object):

    def __init__(self, width, height):
        self.glCreateWindow(width, height)
        self.window_color = Color.black()
        self.draw_color = Color.white()
        self.glClear()

    @staticmethod
    def glInit(width, height):
        return Render(width, height)

    def data(self):
        print("Window")
        print(self.width)
        print(self.height)
        print("ViewPort")
        print(self.viewPort_width)
        print(self.viewPort_height)
        print(self.viewPort_x)
        print(self.viewPort_y)

    def glCreateWindow(self, width, height):
        self.width, self.height = width, height
        Render.glViewPort(self, 0, 0, width, height)

    def glViewPort(self, x, y, width, height):
        self.viewPort_x, self.viewPort_y = x, y
        self.viewPort_width = width if width < self.width else self.width 
        self.viewPort_height = height if height < self.height else self.height
        self.viewPort = [ [ Color.black() for y in range(self.viewPort_height) ] for x in range(self.viewPort_width) ]
        self.glClear()

    def glClear(self, r = 0, g = 0, b = 0):
        self.pixels = [ [ Color.color(int(r * 255), int(g * 255), int(b * 255)) for y in range(self.height) ] for x in range(self.width) ]

    def glClearWhite(self):
        self.glClear(1, 1, 1)

    def glClearColor(self, r, g, b):
        self.glClear(r, g, b)

    def glVertex(self, x, y):
        x_relative, y_relative = self.ndp_to_pixels(x, y)
        try:
            self.viewPort[y_relative][x_relative] = self.draw_color
        except:
            pass

    def glVertex_coords(self, x, y):
        try:
            self.viewPort[y][x] = self.draw_color
        except:
            pass

    def glColor(self, r = 0, g = 0, b = 0):
        self.draw_color = Color.color(int(r * 255), int(g * 255), int(b * 255))

    def glFinish(self, filename = 'output.bmp'):
        render = open(filename, 'wb')

        # File header 14 bytes
        render.write(MemorySize.char('B'))
        render.write(MemorySize.char('M'))
        render.write(MemorySize.dword(14 + 40 + self.width * self.height * 3))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(14 + 40))

        # Image header 40 bytes
        render.write(MemorySize.dword(40))
        render.write(MemorySize.dword(self.width))
        render.write(MemorySize.dword(self.height))
        render.write(MemorySize.word(1))
        render.write(MemorySize.word(24))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(self.width * self.height * 3))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(0))

        Render.insert_viewPort(self)
        
        # Pixels. 3 bytes each
        [ [ render.write(self.pixels[x][y]) for y in range(self.height) ] for x in range(self.width) ]
        render.close()

    def insert_viewPort(self):
        # Insert view port into window
        for x in range(self.viewPort_width):
            for y in range(self.viewPort_height):
                self.pixels[x + self.viewPort_x][y + self.viewPort_y] = self.viewPort[x][y]

    def ndp_to_pixels(self, x, y):
        # Las coordenadas x, y son relativas al viewport.
        return glmath.relative(x, -1, 1, self.viewPort_width, 1) - 1, glmath.relative(y, -1, 1, self.viewPort_height, 1) - 1

    def glLine(self, x0, y0, x1, y1):
        x0, y0 = self.ndp_to_pixels(x0, y0)
        x1, y1 = self.ndp_to_pixels(x1, y1)
        dx, dy = x1 - x0, y1 - y0
        incYi = 1 if dy >= 0 else -1
        incXi = 1 if dx >= 0 else -1
        dx, dy = abs(dx), abs(dy)
        xIncx, xIncy, yIncx, yIncy, dx, dy = (incXi, 0, 0, incYi, dx, dy) if dx >= dy else (0, incYi, incXi, 0, dy, dx)
        y, av = 0, 2 * dy - dx

        for x in range(dx + 1):
            self.glVertex_coords(x0 + x*xIncx + y*yIncx, y0 + x*xIncy + y*yIncy)
            y, av = (y + 1, av - dx) if av >= 0 else (y, av)
            av += dy

    def glLine_coords(self, x0, y0, x1, y1):
        dx, dy = x1 - x0, y1 - y0
        incYi = 1 if dy >= 0 else -1
        incXi = 1 if dx >= 0 else -1
        dx, dy = abs(dx), abs(dy)
        xIncx, xIncy, yIncx, yIncy, dx, dy = (incXi, 0, 0, incYi, dx, dy) if dx >= dy else (0, incYi, incXi, 0, dy, dx)
        y, av = 0, 2 * dy - dx

        for x in range(dx + 1):
            self.glVertex_coords(x0 + x*xIncx + y*yIncx, y0 + x*xIncy + y*yIncy)
            y, av = (y + 1, av - dx) if av >= 0 else (y, av)
            av += dy

    def load_model(self, filename, translate, scale):
        model = Obj(filename)
        posX, posY = self.ndp_to_pixels(translate[0], translate[1])

        for face in model.faces:
            vertex_count = len(face)
            for vertex in range(vertex_count):
                v0 = model.vertices[ face[vertex][0] - 1 ]
                v1 = model.vertices[ face[(vertex + 1) % vertex_count][0] - 1 ]

                x0 = round(v0[0] * scale[0] + posX)
                y0 = round(v0[1] * scale[1] + posY)
                x1 = round(v1[0] * scale[0] + posX)
                y1 = round(v1[1] * scale[1] + posY)

                self.glLine_coords(x0, y0, x1, y1)

    def polygone(self, vertices):
        if len(vertices) < 3: return False
        polygone = Polygone(self, vertices)
        polygone.draw_polygone()
        for x in range(self.viewPort_width):
            for y in range(self.viewPort_height):
                if polygone.has(x, y): self.glVertex_coords(x, y)
