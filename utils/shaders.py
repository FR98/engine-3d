
# def gourad(render, **kwargs):
#     u, v, w = kwargs['baryCoords']
#     ta, tb, tc = kwargs['texCoords']
#     na, nb, nc = kwargs['normals']
#     b, g, r = kwargs['color']

#     b /= 255
#     g /= 255
#     r /= 255

#     if render.active_texture:
#         tx = ta.x * u + tb.x * v + tc.x * w
#         ty = ta.y * u + tb.y * v + tc.y * w
#         texColor = render.active_texture.getColor(tx, ty)
#         b *= texColor[0] / 255
#         g *= texColor[1] / 255
#         r *= texColor[2] / 255

#     nx = na[0] * u + nb[0] * v + nc[0] * w
#     ny = na[1] * u + nb[1] * v + nc[1] * w
#     nz = na[2] * u + nb[2] * v + nc[2] * w

#     normal = V3(nx, ny, nz)

#     intensity = np.dot(normal, render.light)

#     b *= intensity
#     g *= intensity
#     r *= intensity

#     if intensity > 0:
#         return r, g, b
#     else:
#         return 0,0,0

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

    normal = (nx, ny, nz)

    # intensity = glmath.dot(normal, render.light['x'], render.light['y'], render.light['z'])
    intensity = ((normal[0] * render.light['x']) + (normal[1] * render.light['y']) + (normal[2] * render.light['z']))
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