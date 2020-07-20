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