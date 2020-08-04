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

import numpy as np


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
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]

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

    def glVertex_coords(self, x, y, color = None):
        if color == None:
            color = self.draw_color
        try:
            self.viewPort[y][x] = color
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

    def transform(self, vertex, translate=None, scale=None):
        if translate == None:
            translate = self.vector(0, 0, 0)

        if scale == None:
            scale = self.vector(1, 1, 1)
        
        return self.vector(round(vertex[0] * scale['x'] + translate['x']),
                  round(vertex[1] * scale['y'] + translate['y']),
                  round(vertex[2] * scale['z'] + translate['z']))
    
    def loadModel(self, filename, translate = None, scale = None, texture = None,  isWireframe = False):
        if translate == None:
            translate = self.vector(0, 0, 0)

        if scale == None:
            scale = self.vector(0, 0, 0)
        
        model = Obj(filename)

        light = self.vector(0,0,1)

        for face in model.faces:

            vertCount = len(face)

            if isWireframe:
                for vert in range(vertCount):
                    v0 = model.vertices[ face[vert][0] - 1 ]
                    v1 = model.vertices[ face[(vert + 1) % vertCount][0] - 1]
                    v0 = self.vector(round(v0[0] * scale['x']  + translate['x']),round(v0[1] * scale['y']  + translate['y']))
                    v1 = self.vector(round(v1[0] * scale['x']  + translate['x']),round(v1[1] * scale['y']  + translate['y']))
                    self.glLine_coords(v0['x'], v0['y'], v1['x'], v1['y'])
            else:
                v0 = model.vertices[ face[0][0] - 1 ]
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 = model.vertices[ face[2][0] - 1 ]
                if vertCount > 3:
                    v3 = model.vertices[ face[3][0] - 1 ]

                v0 = self.transform(v0,translate, scale)
                v1 = self.transform(v1,translate, scale)
                v2 = self.transform(v2,translate, scale)
                if vertCount > 3:
                    v3 = self.transform(v3,translate, scale)

                if texture:
                    vt0 = model.texture_coords[face[0][1] - 1]
                    vt1 = model.texture_coords[face[1][1] - 1]
                    vt2 = model.texture_coords[face[2][1] - 1]
                    vt0 = self.vector(vt0[0], vt0[1])
                    vt1 = self.vector(vt1[0], vt1[1])
                    vt2 = self.vector(vt2[0], vt2[1])
                    if vertCount > 3:
                        vt3 = model.texture_coords[face[3][1] - 1]
                        vt3 = self.vector(vt3[0], vt3[1])
                else:
                    vt0 = self.vector(0, 0)
                    vt1 = self.vector(0, 0)
                    vt2 = self.vector(0, 0)
                    vt3 = self.vector(0, 0)

                normal = np.cross(np.subtract((v1['x'], v1['y'], v1['z']), (v0['x'], v0['y'], v0['z'])), np.subtract((v2['x'], v2['y'], v2['z']),(v0['x'], v0['y'], v0['z'])))
                normal = normal / np.linalg.norm(normal)
                intensity = np.dot(normal, (light['x'], light['y'], light['z']))

                if intensity >=0:
                    self.triangle_bc(v0,v1,v2, texture = texture, texcoords = (vt0,vt1,vt2), intensity = intensity )
                    if vertCount > 3: #asumamos que 4, un cuadrado
                        self.triangle_bc(v0,v2,v3, texture = texture, texcoords = (vt0,vt2,vt3), intensity = intensity)

    def polygone(self, vertices):
        if len(vertices) < 3: return False
        polygone = Polygone(self, vertices)
        polygone.draw_polygone()
        for x in range(self.viewPort_width):
            for y in range(self.viewPort_height):
                if polygone.has(x, y): self.glVertex_coords(x, y)

    def glZBuffer(self, filename='zbuffer.bmp'):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(MemorySize.dword(14 + 40 + self.width * self.height * 3))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(MemorySize.dword(40))
        archivo.write(MemorySize.dword(self.width))
        archivo.write(MemorySize.dword(self.height))
        archivo.write(MemorySize.word(1))
        archivo.write(MemorySize.word(24))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(self.width * self.height * 3))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                print(depth)
                archivo.write(Color.color(depth,depth,depth))

        archivo.close()

    # def drawPoly(self, points, color = None):
    #     count = len(points)
    #     for i in range(count):
    #         v0 = points[i]
    #         v1 = points[(i + 1) % count]
    #         self.glLine_coords(v0, v1, color)

    def triangle(self, A, B, C, color = None):
        
        def flatBottomTriangle(v1,v2,v3):
            #self.drawPoly([v1,v2,v3], color)
            for y in range(v1.y, v3.y + 1):
                xi = round( v1.x + (v3.x - v1.x)/(v3.y - v1.y) * (y - v1.y))
                xf = round( v2.x + (v3.x - v2.x)/(v3.y - v2.y) * (y - v2.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.glVertex_coords(x,y, color)

        def flatTopTriangle(v1,v2,v3):
            for y in range(v1.y, v3.y + 1):
                xi = round( v2.x + (v2.x - v1.x)/(v2.y - v1.y) * (y - v2.y))
                xf = round( v3.x + (v3.x - v1.x)/(v3.y - v1.y) * (y - v3.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.glVertex_coords(x,y, color)

        # A.y <= B.y <= Cy
        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y:
            B, C = C, B

        if A.y == C.y:
            return

        if A.y == B.y: #En caso de la parte de abajo sea plana
            flatBottomTriangle(A,B,C)
        elif B.y == C.y: #En caso de que la parte de arriba sea plana
            flatTopTriangle(A,B,C)
        else: #En cualquier otro caso
            # y - y1 = m * (x - x1)
            # B.y - A.y = (C.y - A.y)/(C.x - A.x) * (D.x - A.x)
            # Resolviendo para D.x
            x4 = A.x + (C.x - A.x)/(C.y - A.y) * (B.y - A.y)
            D = self.vector(round(x4), B.y)
            flatBottomTriangle(D,B,C)
            flatTopTriangle(A,B,D)

    #Barycentric Coordinates
    def triangle_bc(self, A, B, C, _color = Color.white, texture = None, texcoords = (), intensity = 1):
        #bounding box
        minX = min(A['x'], B['x'], C['x'])
        minY = min(A['y'], B['y'], C['y'])
        maxX = max(A['x'], B['x'], C['x'])
        maxY = max(A['y'], B['y'], C['y'])

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if x >= self.width or x < 0 or y >= self.height or y < 0:
                    continue

                u, v, w = glmath.baryCoords(A, B, C, self.vector(x, y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w
                    if z > self.zbuffer[y][x]:
                        
                        b, g , r = _color
                        b /= 255
                        g /= 255
                        r /= 255

                        b *= intensity
                        g *= intensity
                        r *= intensity

                        if texture:
                            ta, tb, tc = texcoords
                            tx = ta.x * u + tb.x * v + tc.x * w
                            ty = ta.y * u + tb.y * v + tc.y * w

                            texColor = texture.getColor(tx, ty)
                            b *= texColor[0] / 255
                            g *= texColor[1] / 255
                            r *= texColor[2] / 255

                        self.glVertex_coords(x, y, Color.color(r,g,b))
                        self.zbuffer[y][x] = z

    def vector(self, x, y, z=0, w=0):
        return {
            "x": x,
            "y": y,
            "z": z,
            "w": w
        }
