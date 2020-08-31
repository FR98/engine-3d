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
from numpy import cos, sin, tan, pi


class Render(object):

    def __init__(self, width, height):
        self.glCreateWindow(width, height)
        self.window_color = Color.black()
        self.draw_color = Color.white()
        self.glClear()
        self.light = self.vector(0, 0, 1)
        self.active_texture = None
        self.active_texture2 = None
        self.active_shader = None

        self.createViewMatrix()
        self.createProjectionMatrix()

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

    def createViewMatrix(self, camPosition=None, camRotation=None):
        camPosition = self.vector(0, 0, 0) if not camPosition else camPosition
        camRotation = self.vector(0, 0, 0) if not camRotation else camRotation
        camMatrix = self.createModelMatrix(translate=camPosition, rotate=camRotation)
        self.viewMatrix = glmath.inverse(camMatrix)

    def createProjectionMatrix(self, n=0.1, f=1000, fov=60):
        t = tan((fov * pi / 180) / 2) * n
        r = t * self.viewPort_width / self.viewPort_height

        self.projectionMatrix = [
            [n / r, 0, 0, 0],
            [0, n / t, 0, 0],
            [0, 0, -(f + n) / (f - n), -(2 * f * n) / (f - n)],
            [0, 0, -1, 0]
        ]

    def lookAt(self, eye, camPosition=None):
        camPosition = self.vector(0, 0, 0) if not camPosition else camPosition

        forward = glmath.sub(camPosition, eye)
        forward = glmath.div(forward, glmath.frobeniusNorm(forward))

        right = glmath.cross(self.vector(0,1,0), forward)
        right = glmath.div(right, glmath.frobeniusNorm(right))

        up = glmath.cross(forward, right)
        up = glmath.div(up, glmath.frobeniusNorm(up))

        camMatrix = [
            [round(right['x']), round(up['x']), round(forward['x']), round(camPosition['x'])],
            [round(right['y']), round(up['y']), round(forward['y']), round(camPosition['y'])],
            [round(right['z']), round(up['z']), round(forward['z']), round(camPosition['z'])],
            [0,0,0,1]
        ]

        self.viewMatrix = glmath.inverse(camMatrix)

    def glCreateWindow(self, width, height):
        self.width, self.height = width, height
        self.glClear()
        Render.glViewPort(self, 0, 0, width, height)

    def glViewPort(self, x, y, width, height):
        self.viewPort_x, self.viewPort_y = x, y
        self.viewPort_width = width if width < self.width else self.width 
        self.viewPort_height = height if height < self.height else self.height
        self.viewPort = [ [ Color.black() for y in range(self.viewPort_height) ] for x in range(self.viewPort_width) ]
        self.glClear()

        self.viewportMatrix = [
                [self.viewPort_width / 2, 0, 0, x + self.viewPort_width / 2],
                [0, self.viewPort_height / 2, 0, y + self.viewPort_height / 2],
                [0, 0, 0.5, 0.5],
                [0, 0, 0, 1]
            ]

    def glClear(self, r = 0, g = 0, b = 0):
        self.pixels = [ [ Color.color(r, g, b) for y in range(self.height) ] for x in range(self.width) ]
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glClearWhite(self):
        self.glClear(1, 1, 1)

    def glClearColor(self, r, g, b):
        self.glClear(r, g, b)

    def glVertex(self, x, y, color=None):
        x_relative, y_relative = self.ndp_to_pixels(x, y)
        try:
            self.viewPort[y_relative][x_relative] = color or self.draw_color
        except:
            pass

    def glVertex_coords(self, x, y, color=None):
        if color == None:
            color = self.draw_color
        try:
            self.viewPort[y][x] = color
        except:
            pass

    def glColor(self, r = 0, g = 0, b = 0):
        self.draw_color = Color.color(r, g, b)

    def glFinish(self, filename = 'output/output.bmp'):
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

    def load_model_3D(self, filename, translate=None, scale=None, rotate=None, isWireframe=False):
        translate = self.vector(0, 0, 0) if not translate else translate
        scale = self.vector(1, 1, 1) if not scale else scale
        rotate = self.vector(0, 0, 0) if not rotate else rotate

        model = Obj(filename)
        posX, posY = self.ndp_to_pixels(translate['x'], translate['y'])
        translate = self.vector(posX, posY, 0)

        modelMatrix = self.createModelMatrix(translate, scale, rotate)
        rotationMatrix = self.createRotationMatrix(rotate)

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

                v0 = self.transform(self.vector(v0[0], v0[1], v0[2]), modelMatrix)
                v1 = self.transform(self.vector(v1[0], v1[1], v1[2]), modelMatrix)
                v2 = self.transform(self.vector(v2[0], v2[1], v2[2]), modelMatrix)
                vA, vB, vC = v0, v1, v2

                v0 = self.camTransform(v0)
                v1 = self.camTransform(v1)
                v2 = self.camTransform(v2)

                if vertex_count > 3:
                    v3 = self.transform(self.vector(v3[0], v3[1], v3[2]), modelMatrix)
                    vD = v3
                    v3 = self.camTransform(v3)

                if self.active_texture:
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

                try:
                    vn0 = model.normals[face[0][2] - 1]
                    vn1 = model.normals[face[1][2] - 1]
                    vn2 = model.normals[face[2][2] - 1]
                    vn0 = self.dirTransform(self.vector(vn0[0], vn0[1], vn0[2]), rotationMatrix)
                    vn1 = self.dirTransform(self.vector(vn1[0], vn1[1], vn1[2]), rotationMatrix)
                    vn2 = self.dirTransform(self.vector(vn2[0], vn2[1], vn2[2]), rotationMatrix)
                    if vertex_count > 3:
                        vn3 = model.normals[face[3][2] - 1]
                        vn3 = self.dirTransform(self.vector(vn3[0], vn3[1], vn3[2]), rotationMatrix)
                except:
                    pass

                self.triangle_bc(vA,vB,vC, texcoords=(vt0,vt1,vt2), normals=(vn0,vn1,vn2))
                if vertex_count > 3:
                    self.triangle_bc(vA,vB,vD, texcoords=(vt0,vt2,vt3), normals=(vn0,vn2,vn3))

    def transform(self, vertex, vMatrix):
        augVertex = (vertex['x'], vertex['y'], vertex['z'], 1)
        transVertex = glmath.multiplicarMatrizVector(augVertex, vMatrix)
        transVertex = self.vector(transVertex[0] / transVertex[3],
                       transVertex[1] / transVertex[3],
                       transVertex[2] / transVertex[3])
        return transVertex

    def camTransform(self, vertex):
        augVertex = (vertex['x'], vertex['y'], vertex['z'], 1)
        transVertex1 = glmath.multiplicarMatrices(self.viewportMatrix, self.projectionMatrix)
        transVertex2 = glmath.multiplicarMatrices(transVertex1, self.viewMatrix)
        transVertex = glmath.multiplicarMatrizVector(augVertex, transVertex2)
        return self.vector(transVertex[0] / transVertex[3], transVertex[1] / transVertex[3], transVertex[2] / transVertex[3])

    def dirTransform(self, vertex, vMatrix):
        augVertex = (vertex['x'], vertex['y'], vertex['z'], 0)
        transVertex = glmath.multiplicarMatrizVector(augVertex, vMatrix)
        return self.vector(transVertex[0], transVertex[1], transVertex[2])

    def createModelMatrix(self, translate=None, scale=None, rotate=None):
        translate = self.vector(0, 0, 0) if not translate else translate
        scale = self.vector(1, 1, 1) if not scale else scale
        rotate = self.vector(0, 0, 0) if not rotate else rotate

        translateMatrix = [
            [1, 0, 0, translate['x']],
            [0, 1, 0, translate['y']],
            [0, 0, 1, translate['z']],
            [0, 0, 0, 1]
        ]

        scaleMatrix = [
            [scale['x'], 0, 0, 0],
            [0, scale['y'], 0, 0],
            [0, 0, scale['z'], 0],
            [0, 0, 0, 1]
        ]

        rotationMatrix = self.createRotationMatrix(rotate)
        finalObjectMatrix = glmath.multiplicarMatrices(translateMatrix, rotationMatrix)
        return glmath.multiplicarMatrices(finalObjectMatrix, scaleMatrix)

    def createRotationMatrix(self, rotate=None):
        rotate = self.vector(0, 0, 0) if not rotate else rotate
        pitch = glmath.degToRad(rotate['x'])
        yaw = glmath.degToRad(rotate['y'])
        roll = glmath.degToRad(rotate['z'])

        rotationX = [
            [1, 0, 0, 0],
            [0, cos(pitch), -sin(pitch), 0],
            [0, sin(pitch), cos(pitch), 0],
            [0, 0, 0, 1]
        ]

        rotationY = [
            [cos(yaw), 0, sin(yaw), 0],
            [0, 1, 0, 0],
            [-sin(yaw), 0, cos(yaw), 0],
            [0, 0, 0, 1]
        ]

        rotationZ = [
            [cos(roll), -sin(roll), 0, 0],
            [sin(roll), cos(roll), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        finalMatrixRotation = glmath.multiplicarMatrices(rotationX, rotationY)
        return glmath.multiplicarMatrices(finalMatrixRotation, rotationZ)

    def triangle_bc(self, A, B, C, texcoords, color=None, normals=()):
        minX = int(min(A['x'], B['x'], C['x']))
        minY = int(min(A['y'], B['y'], C['y']))
        maxX = int(max(A['x'], B['x'], C['x']))
        maxY = int(max(A['y'], B['y'], C['y']))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if x >= self.width or x < 0 or y >= self.height or y < 0:
                    continue

                u, v, w = glmath.baryCoords(A, B, C, self.vector(x, y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A['z'] * u + B['z'] * v + C['z'] * w

                    if z > self.zbuffer[y][x]:
                        if self.active_shader:

                            r, g, b = self.active_shader(
                                self,
                                # verts = verts,
                                baryCoords = (u,v,w),
                                texCoords = texcoords,
                                normals = normals,
                                color = color or self.draw_color
                            )
                        else:
                            b, g, r = color or self.draw_color

                        self.glVertex_coords(x, y, Color.color(r, g, b))
                        self.zbuffer[y][x] = z

    def glZBuffer(self, filename='output/zbuffer.bmp'):
        archivo = open(filename, 'wb')

        height, width = self.height, self.width

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(MemorySize.dword(14 + 40 + width * height * 3))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(MemorySize.dword(40))
        archivo.write(MemorySize.dword(width))
        archivo.write(MemorySize.dword(height))
        archivo.write(MemorySize.word(1))
        archivo.write(MemorySize.word(24))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(width * height * 3))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))

        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(height):
            for y in range(width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(height):
            for y in range(width):
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
