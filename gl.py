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
        self.active_shader = None

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

    def polygone(self, vertices):
        if len(vertices) < 3: return False
        polygone = Polygone(self, vertices)
        polygone.draw_polygone()
        for x in range(self.viewPort_width):
            for y in range(self.viewPort_height):
                if polygone.has(x, y): self.glVertex_coords(x, y)

    def load_model_2D(self, filename, translate, scale):
        model = Obj(filename)
        posX, posY = self.ndp_to_pixels(translate['x'], translate['y'])

        for face in model.faces:
            vertex_count = len(face)
            for vertex in range(vertex_count):
                v0 = model.vertices[ face[vertex][0] - 1 ]
                v1 = model.vertices[ face[(vertex + 1) % vertex_count][0] - 1 ]

                x0, y0 = round(v0[0] * scale['x'] + posX), round(v0[1] * scale['y'] + posY)
                x1, y1 = round(v1[0] * scale['x'] + posX), round(v1[1] * scale['y'] + posY)
                self.glLine_coords(x0, y0, x1, y1)

    def load_model_3D(self, filename, translate, scale, light, texture=None, isWireframe=False):
        model = Obj(filename)
        posX, posY = self.ndp_to_pixels(translate['x'], translate['y'])

        for face in model.faces:
            vertex_count = len(face)

            if isWireframe:
                for vert in range(vertex_count):
                    v0 = model.vertices[face[vert][0] - 1]
                    v1 = model.vertices[face[(vert + 1) % vertex_count][0] - 1]
                    v0 = self.vector(round(v0[0] * scale['x'] + translate['x']), round(v0[1] * scale['y'] + translate['y']))
                    v1 = self.vector(round(v1[0] * scale['x'] + translate['x']), round(v1[1] * scale['y'] + translate['y']))
                    self.glLine_coords(v0['x'], v0['y'], v1['x'], v1['y'])

            else:
                v0 = model.vertices[ face[0][0] - 1 ]
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 = model.vertices[ face[2][0] - 1 ]
                if vertex_count > 3:
                    v3 = model.vertices[ face[3][0] - 1 ]

                x0, y0, z0 = int(v0[0] * scale['x']  + translate['x']), int(v0[1] * scale['y']  + translate['y']), int(v0[2] * scale['z']  + translate['z'])
                x1, y1, z1 = int(v1[0] * scale['x']  + translate['x']), int(v1[1] * scale['y']  + translate['y']), int(v1[2] * scale['z']  + translate['z'])
                x2, y2, z2 = int(v2[0] * scale['x']  + translate['x']), int(v2[1] * scale['y']  + translate['y']), int(v2[2] * scale['z']  + translate['z'])
                v0 = self.transform(self.vector(x0, y0, z0), translate, scale)
                v1 = self.transform(self.vector(x1, y1, z1), translate, scale)
                v2 = self.transform(self.vector(x2, y2, z2), translate, scale)
                # v0 = self.transform(self.vector(v0[0], v0[1], v0[2]), translate, scale)
                # v1 = self.transform(self.vector(v1[0], v1[1], v1[2]), translate, scale)
                # v2 = self.transform(self.vector(v2[0], v2[1], v2[2]), translate, scale)
                if vertex_count > 3:
                    v3 = self.transform(v3, translate, scale)

                if texture:
                    vt0 = model.texture_coords[face[0][1] - 1]
                    vt1 = model.texture_coords[face[1][1] - 1]
                    vt2 = model.texture_coords[face[2][1] - 1]
                    vt0 = self.vector(vt0[0], vt0[1])
                    vt1 = self.vector(vt1[0], vt1[1])
                    vt2 = self.vector(vt2[0], vt2[1])
                    if vertex_count > 3:
                        vt3 = model.texture_coords[face[3][1] - 1]
                        vt3 = self.vector(vt3[0], vt3[1])
                else:
                    vt0 = self.vector(0, 0)
                    vt1 = self.vector(0, 0)
                    vt2 = self.vector(0, 0)
                    vt3 = self.vector(0, 0)

                # import numpy as np

                sub1 = glmath.sub(x1, x0, y1, y0, z1, z0)
                sub2 = glmath.sub(x2, x0, y2, y0, z2, z0)
                cross1 = glmath.cross(sub1, sub2 )
                norm1 = glmath.norm(cross1)
                cross2 = glmath.cross(sub1, sub2)

                normal = glmath.div(cross2, norm1)
                # normal = np.cross(np.subtract(v1,v0), np.subtract(v2,v0))
                # normal = normal / np.linalg.norm(normal)
                # intensity = np.dot(normal, light)

                intensity = round(glmath.dot(normal, light['x'], light['y'], light['z']))

                if intensity >= 0:
                    self.triangle_bc(self.vector(x0, y0, z0), self.vector(x1, y1, z1), self.vector(x2, y2, z2), intensity=intensity)
                
                if vertex_count > 3: 
                    v3 = model.vertices[face[3][0] - 1]
                    x3, y3, z3 = int(v3[0] * scale['x']  + translate['x']), int(v3[1] * scale['y']  + translate['y']), int(v3[2] * scale['z']  + translate['z'])

                    if intensity >= 0:
                        self.triangle_bc(self.vector(x0, y0, z0), self.vector(x2, y2, z2), self.vector(x3, y3, z3), intensity=intensity)

                # if intensity >=0:
                #     self.triangle_bc(v0,v1,v2, texture = texture, texcoords = (vt0,vt1,vt2), intensity = intensity )
                #     if vertex_count > 3: #asumamos que 4, un cuadrado
                #         self.triangle_bc(v0,v2,v3, texture = texture, texcoords = (vt0,vt2,vt3), intensity = intensity)

    def transform(self, vertex, translate=None, scale=None):
        if translate == None:
            translate = self.vector(0, 0, 0)

        if scale == None:
            scale = self.vector(1, 1, 1)

        return self.vector(round(vertex['x'] * scale['x'] + translate['x']), round(vertex['y'] * scale['y'] + translate['y']), round(vertex['z'] * scale['z'] + translate['z']))


    def triangle_bc(self, A, B, C, color=Color.white(), normals=(), texture=None, texcoords=None, intensity=1):
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

                    z = A['z'] * u + B['z'] * v + C['z'] * w

                    if z > self.zbuffer[y][x]:
                        r, g, b = self.active_shader(
                            self,
                            verts=(A,B,C),
                            baryCoords=(u,v,w),
                            texCoords=texcoords,
                            normals=normals,
                            color = color or self.draw_color)
                        
                        self.glVertex_coords(x, y, color)
                        self.zbuffer[y][x] = z


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
                archivo.write(Color.color(depth,depth,depth))

        archivo.close()

    def vector(self, x, y, z=0, w=0):
        return {
            "x": x,
            "y": y,
            "z": z,
            "w": w
        }




def gourad(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = np.dot(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def sombreadoCool(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = np.dot(normal, render.light)
    if intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if render.active_texture2:
        texColor = render.active_texture2.getColor(tx, ty)

        b += (texColor[0] / 255) * (1 - intensity)
        g += (texColor[1] / 255) * (1 - intensity)
        r += (texColor[2] / 255) * (1 - intensity)


    return r, g, b