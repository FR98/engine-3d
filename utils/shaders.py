import utils.glmath as glmath
import random

def gourad(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta['x'] * u + tb['x'] * v + tc['x'] * w
        ty = ta['y'] * u + tb['y'] * v + tc['y'] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = render.vector(nx, ny, nz)
    intensity = glmath.dot(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
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
        tx = ta['x'] * u + tb['x'] * v + tc['x'] * w
        ty = ta['y'] * u + tb['y'] * v + tc['y'] * w
        texColor = render.active_texture.getColor(tx, ty)
        
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = render.vector(nx, ny, nz)
    intensity = glmath.dot(normal, render.light)

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


def toon(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta['x'] * u + tb['x'] * v + tc['x'] * w
        ty = ta['y'] * u + tb['y'] * v + tc['y'] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = render.vector(nx, ny, nz)
    intensity = glmath.dot(normal, render.light)

    if (intensity >= 0 and intensity <= 0.25):
        intensity = 0.25
    elif (intensity > 0.25 and intensity <= 0.5):
        intensity = 0.5
    elif (intensity > 0.5 and intensity <= 0.75):
        intensity = 0.75
    elif (intensity > 0.75):
        intensity = 1
    else:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    return 0,0,0


def heat(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta['x'] * u + tb['x'] * v + tc['x'] * w
        ty = ta['y'] * u + tb['y'] * v + tc['y'] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = render.vector(nx, ny, nz)
    intensity = glmath.dot(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if (intensity >= 0 and intensity <= 0.2):
        # Azul
        return r*0.25, g*0.25, b
    elif (intensity > 0.2 and intensity <= 0.4):
        # Verde
        return r*0.25, g, b*0.25
    elif (intensity > 0.4 and intensity <= 0.6):
        # Amarillo
        return r, g, b*0.25
    elif (intensity > 0.6 and intensity <= 0.8):
        # Naranja
        return r, g*0.5, b*0.25
    elif (intensity > 0.8):
        # Rojo
        return r, g*0.25, b*0.25

    if intensity > 0:
        return r, g, b
    return 0,0,0


def randomPattern(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta['x'] * u + tb['x'] * v + tc['x'] * w
        ty = ta['y'] * u + tb['y'] * v + tc['y'] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = render.vector(nx, ny, nz)
    intensity = glmath.dot(normal, render.light)

    randomNumber = random.randint(0, 100)

    if (intensity >= 0 and intensity <= 1):
        intensity = intensity * randomNumber/100
    else:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    return 0,0,0


def underwater(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta['x'] * u + tb['x'] * v + tc['x'] * w
        ty = ta['y'] * u + tb['y'] * v + tc['y'] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = render.vector(nx, ny, nz)
    intensity = glmath.dot(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if (intensity >= 0 and intensity <= 0.2):
        return r*0, g*0, b*0
    elif (intensity > 0.2 and intensity <= 0.4):
        return r*0, g*0.1, b
    elif (intensity > 0.4 and intensity <= 0.6):
        return r*0, g*0.2, b
    elif (intensity > 0.6 and intensity <= 0.8):
        return r*0.1, g*0.3, b
    elif (intensity > 0.8):
        return r*0.75, g, b

    if intensity > 0:
        return r, g, b
    return 0,0,0


def grayscale(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta['x'] * u + tb['x'] * v + tc['x'] * w
        ty = ta['y'] * u + tb['y'] * v + tc['y'] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = render.vector(nx, ny, nz)
    intensity = glmath.dot(normal, render.light)

    if (intensity >= 0 and intensity <= 1):
        pass
    else:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    c = min([b, g, r])

    if intensity > 0:
        return c, c, c
    return 0,0,0
