
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

# Suma de vectores de 3 elementos
def sum(x0, x1, y0, y1, z0, z1):
    arr_sum = []
    arr_sum.extend((x0 + x1, y0 + y1, z0 + z1))
    return arr_sum

# Resta de vectores de 3 elementos
def sub(x0, x1, y0, y1, z0, z1):
    arr_sub = []
    arr_sub.extend((x0 - x1, y0 - y1, z0 - z1))
    return arr_sub
    
# Producto cruz entre dos vectores
def cross(v0, v1):
    arr_cross = []
    arr_cross.extend((v0[1] * v1[2] - v1[1] * v0[2], -(v0[0] * v1[2] - v1[0] * v0[2]), v0[0] * v1[1] - v1[0] * v0[1]))
    return arr_cross

# Producto punto (utilizado para la matriz con las coordenadas de luz)
def dot(norm, lX, lY, lZ):
    return ((norm[0] * lX) + (norm[1] * lY) + (norm[2] * lZ))

# Calculo de la normal de un vector
def norm(v0):
    if (v0 == 0):
        arr0_norm = []
        arr0_norm.extend((0,0,0))
        return arr0_norm

    return((v0[0]**2 + v0[1]**2 + v0[2]**2)**(1/2))

# Division vector con normal
def div(v0, norm):
    if (norm == 0):
        arr0_norm = []
        arr0_norm.extend((0,0,0))
        return arr0_norm
    else:
        arr_div = []
        arr_div.extend((v0[0] / norm, v0[1] / norm, v0[2] / norm))
        return arr_div