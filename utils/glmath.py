
def relative(user_input, input_low, input_high, output_high, output_low):
    return int(( (user_input - input_low) / (input_high - input_low) ) * (output_high - output_low) + output_low)


def baryCoords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((B['y'] - C['y'])*(P['x'] - C['x']) + (C['x'] - B['x'])*(P['y'] - C['y']) ) /
              ((B['y'] - C['y'])*(A['x'] - C['x']) + (C['x'] - B['x'])*(A['y'] - C['y'])) )

        v = ( ((C['y'] - A['y'])*(P['x'] - C['x']) + (A['x'] - C['x'])*(P['y'] - C['y']) ) /
              ((B['y'] - C['y'])*(A['x'] - C['x']) + (C['x'] - B['x'])*(A['y'] - C['y'])) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

def sum(x0, x1, y0, y1, z0, z1):
    sum = []
    sum.extend((x0 + x1, y0 + y1, z0 + z1))
    return sum

def sub(x0, x1, y0, y1, z0, z1):
    sub = []
    sub.extend((x0 - x1, y0 - y1, z0 - z1))
    return sub

def cross(v0, v1):
    cross = []
    cross.extend((v0[1] * v1[2] - v1[1] * v0[2], -(v0[0] * v1[2] - v1[0] * v0[2]), v0[0] * v1[1] - v1[0] * v0[1]))
    return cross

def dot(norm, lX, lY, lZ):
    return ((norm[0] * lX) + (norm[1] * lY) + (norm[2] * lZ))

def norm(v0):
    if (v0 == 0):
        norm = []
        norm.extend((0,0,0))
        return norm

    return((v0[0]**2 + v0[1]**2 + v0[2]**2)**(1/2))

def div(v0, norm):
    if (norm == 0):
        norm = []
        norm.extend((0,0,0))
        return norm
    else:
        div = []
        div.extend((v0[0] / norm, v0[1] / norm, v0[2] / norm))
        return div
