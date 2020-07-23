from gl import Render

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
    render = Render(3700, 3700)
    # render.load_model('./models/Propeller/Propeller.obj', (0, 0), (0.4, 0.4))
    render.load_model('./models/Biplane/OBJ/HiPoly/Biplane.obj', (0, 0), (450, 450))
    render.glFinish()
