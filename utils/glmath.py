
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

def vector(self, x, y, z=0, w=0):
    return {
        "x": x,
        "y": y,
        "z": z,
        "w": w
    }

def sub(A, B):
    return vector(A['x'] - B['x'], A['y'] - B['y'], A['z'] - B['z'])

def cross(A, B):
    return vector(A['y'] * B['z'] - B['y'] * A['z'], -(A['x'] * B['z'] - B['x'] * A['z']), A['x'] * B['y'] - B['x'] * A['y'])

def dot(norm, l):
    return ((norm['x'] * l['x']) + (norm['y'] * l['y']) + (norm['z'] * l['z']))

def norm(V):
    if (V == 0):
        return vector(0, 0, 0)
    return((V['x']**2 + V['y']**2 + V['z']**2)**(1/2))

def div(V, norm):
    if (norm == 0):
        return vector(0, 0, 0)
    else:
        return vector(V['x'] / norm, V['y'] / norm, V['z'] / norm)
