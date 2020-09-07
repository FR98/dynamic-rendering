"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from numpy import pi

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

def vector(x, y, z=0, w=0):
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

def div(V, norm):
    if (norm == 0):
        return vector(0, 0, 0)
    return vector(V['x'] / norm, V['y'] / norm, V['z'] / norm)

def verificarMultiplicar(MR1, MR2):
	cantColumnasMR1 = len(MR1[0])
	cantFilasMR2 = len(MR2)
	if cantColumnasMR1 == cantFilasMR2:
		return True
	return False

def crearMatrizVacia(m, n):
	matriz = []
	for f in range(0, m):
		fila = []
		for c in range(0, n):
			fila.append(0)
		matriz.append(fila)
	return matriz

def degToRad(n):
    return n * (pi/180)

def multiplicarMatrizVector(V, M):
    result = []
    for i in range(len(M)):
        total = 0
        for j in range(len(V)):
            total += M[i][j] * V[j]
        result.append(total)
    return result

def traspuesta(matriz):
	# Da la traspuesta de una matriz
	cantFilas = len(matriz)
	cantColumnas = len(matriz[0])
	traspuesta = crearMatrizVacia(cantColumnas, cantFilas)
	for f in range(0, cantFilas):
		for c in range(0, cantColumnas):
			traspuesta[c][f] = matriz[f][c]
	return traspuesta

def sumaBinaria(a, b):
	if (a == 0 or b == 0):
		return a + b
	return 1

def multiplicarMatrices(MR1, MR2):
	if (verificarMultiplicar(MR1, MR2)):
		traspuestaMR1 = traspuesta(MR1)
		matrizResultado = []

		for f in range(0, len(MR2[0])):
			vColumna = [0 for i in range(0, len(MR1))]
			for c in range(0, len(MR1[0])):
				v = list(map(lambda x: x * MR2[c][f], traspuestaMR1[c]))
				vTemp = []
				for e in range(0, len(v)):
					vTemp.append(sumaBinaria(v[e], vColumna[e]))
				vColumna = vTemp
			matrizResultado.append(vColumna)

		return traspuesta(matrizResultado)
	return "No se pueden multiplicar"

def eliminate(r1, r2, col, target=0):
    fac = (r2[col]-target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]

def gauss(a):
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i+1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                # print("MATRIX NOT INVERTIBLE")
                return -1
        for j in range(i+1, len(a)):
            eliminate(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminate(a[i], a[j], i)
    for i in range(len(a)):
        eliminate(a[i], a[i], i, target=1)
    return a

def inverse(a):
    tmp = [[] for _ in a]
    for i, row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [0]*i + [1] + [0]*(len(a)-i-1))
    gauss(tmp)
    ret = []
    for i in range(len(tmp)):
        ret.append(tmp[i][len(tmp[i]) // 2:])
    return ret

def frobeniusNorm(v):
	suma = 0
	for i in v.values():
		suma += i ** 2
	return suma ** 0.5
