"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from color import Color
from memory import MemorySize
import glmath


class Render(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window_color = Color.black()
        self.draw_color = Color.white()
        self.glClear()

    @staticmethod
    def glInit(width, height):
        return Render(width, height)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        Render.glViewPort(self, 0, 0, width, height)

    def glViewPort(self, x, y, width, height):
        self.viewPort_x = x
        self.viewPort_y = y
        self.viewPort_width = width
        self.viewPort_height = height
        self.viewPort = [ [ Color.white() for y in range(self.viewPort_height) ] for x in range(self.viewPort_width) ]

    def glClear(self, r = 1, g = 1, b = 1):
        self.pixels = [ [ Color.color(int(r * 255), int(g * 255), int(b * 255)) for y in range(self.height) ] for x in range(self.width) ]

    def glClearBlack(self):
        self.glClear(0, 0, 0)

    def glClearColor(self, r, g, b):
        self.glClear(r, g, b)

    def glVertex(self, x, y):
        # Las coordenadas x, y son relativas al viewport.
        x_relative = glmath.relative(x, -1, 1, self.viewPort_width, 1) - 1
        y_relative = glmath.relative(y, -1, 1, self.viewPort_height, 1) - 1
        # x_relative = int((x + 1) * ((self.viewPort_width-1) / 2) )
        # y_relative = int((y + 1) * ((self.viewPort_height-1) / 2) )
        self.viewPort[y_relative][x_relative] = self.draw_color

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
