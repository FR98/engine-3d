from gl import Render
from obj import Texture
import utils.shaders as shaders

def star(width, height):
    r = Render.glInit(width, height)

    r.glClear()
    r.glColor(1, 1, 1)

    # Lines
    r.glLine(0, 0, 1, 0)
    r.glLine(0, 0, 0, 1)
    r.glLine(0, 0, -1, 0)
    r.glLine(0, 0, 0, -1)


    r.glLine(0, 0, 1, 1)
    r.glLine(0, 0, 1, -1)
    r.glLine(0, 0, -1, 1)
    r.glLine(0, 0, -1, -1)


    r.glLine(0, 0, 0.5, 1)
    r.glLine(0, 0, 1, 0.5)
    r.glLine(0, 0, 1, -0.5)
    r.glLine(0, 0, 0.5, -1)
    r.glLine(0, 0, -0.5, 1)
    r.glLine(0, 0, -1, 0.5)
    r.glLine(0, 0, -1, -0.5)
    r.glLine(0, 0, -0.5, -1)


    r.glLine(0, 0, 0.25, 1)
    r.glLine(0, 0, 0.75, 1)
    r.glLine(0, 0, 1, 0.75)
    r.glLine(0, 0, 1, 0.25)

    r.glLine(0, 0, 0.25, -1)
    r.glLine(0, 0, 0.75, -1)
    r.glLine(0, 0, 1, -0.75)
    r.glLine(0, 0, 1, -0.25)

    r.glLine(0, 0, -0.25, -1)
    r.glLine(0, 0, -0.75, -1)
    r.glLine(0, 0, -1, -0.75)
    r.glLine(0, 0, -1, -0.25)

    r.glLine(0, 0, -0.25, 1)
    r.glLine(0, 0, -0.75, 1)
    r.glLine(0, 0, -1, 0.75)
    r.glLine(0, 0, -1, 0.25)

    r.glFinish()

def biplane():
    render = Render(2000, 2000)
    # render.load_model('./models/Propeller/Propeller.obj', (0, 0), (0.4, 0.4))
    render.load_model_2D('./models/Biplane/OBJ/HiPoly/Biplane.obj', render.vector(0, 0), render.vector(200, 200))
    render.glFinish()

def poligonos():
    poligono1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
    poligono2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
    poligono3 = [(377, 249), (411, 197), (436, 249)]
    poligono4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]
    poligono5 = [(682, 175), (708, 120), (735, 148), (739, 170)]
    render = Render(800, 800)
    render.polygone(poligono1)
    render.polygone(poligono2)
    render.polygone(poligono3)
    render.polygone(poligono4)
    render.polygone(poligono5)
    render.glFinish()

def model_with_triangle():
    render = Render(2000, 2000)
    render.light = render.vector(0, 0, 1)
    render.load_model_3D('./models/Biplane/OBJ/HiPoly/Biplane.obj', scale=render.vector(200, 200, 200), rotate=render.vector(0, 0, 0))
    render.glFinish()

def model_z_buffer():
    render = Render(2000, 2000)
    render.light = render.vector(0, 0, 1)
    # render.load_model_3D('./models/Biplane/OBJ/HiPoly/Biplane.obj', translate=render.vector(0, 0, 0), scale=render.vector(200, 200, 200), light=render.vector(0, 0, 1))
    render.load_model_3D('./models/Face/model.obj', scale=render.vector(200, 200, 200), rotate=render.vector(0, 0, 0))
    # render.glFinish()
    render.glZBuffer()

def model_texture():
    render = Render(2000, 2000)
    render.light = render.vector(0, 0, 1)
    render.active_texture = Texture('./models/Face/model.bmp')
    render.active_shader = shaders.randomPattern
    render.load_model_3D('./models/Face/model.obj', scale=render.vector(200, 200, 200), rotate=render.vector(0, 45, 0))
    render.glFinish()
    render.glZBuffer()
