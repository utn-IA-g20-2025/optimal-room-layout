import math

def calcular_distancia(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )

def fitness(muebles, habitacion, tomas, reglas_adyacencia=[]):
    """
    muebles: lista de muebles/electrodomésticos, cada uno como un dict con keys:
        - 'nombre'
        - 'ancho', 'profundidad'
        - 'x', 'z' (posición)
        - 'rot' (rotación en grados: 0 o 90)
        - 'requiere_toma' (bool)
        - 'debe_ir_a_pared' (bool)
    habitacion: dict con 'ancho', 'profundidad'
    tomas: lista de coordenadas (x, z)
    reglas_adyacencia: lista de tuplas con nombres de objetos que deben estar juntos.
    """

    puntuacion = 1000  # base

    objetos = []

    for mueble in muebles:
        if mueble['rot'] == 90:
            w, d = mueble['profundidad'], mueble['ancho']
        else:
            w, d = mueble['ancho'], mueble['profundidad']

        x, z = mueble['x'], mueble['z']

        if (x < 0 or z < 0 or
            x + w > habitacion['ancho'] or
            z + d > habitacion['profundidad']):
            puntuacion -= 200

        objetos.append({
            'nombre': mueble['nombre'],
            'x1': x, 'z1': z,
            'x2': x + w, 'z2': z + d,
            'cx': x + w / 2, 'cz': z + d / 2,
            'requiere_toma': mueble.get('requiere_toma', False),
            'debe_ir_a_pared': mueble.get('debe_ir_a_pared', False)
        })

    for i in range(len(objetos)):
        for j in range(i + 1, len(objetos)):
            o1, o2 = objetos[i], objetos[j]
            intersecta = not (
                o1['x2'] <= o2['x1'] or o2['x2'] <= o1['x1'] or
                o1['z2'] <= o2['z1'] or o2['z2'] <= o1['z1']
            )
            if intersecta:
                puntuacion -= 300

    for obj in objetos:
        if obj['requiere_toma']:
            dist_min = min([calcular_distancia((obj['cx'], obj['cz']), toma) for toma in tomas])
            puntuacion -= dist_min * 5

    for obj in objetos:
        if obj['debe_ir_a_pared']:
            dist_pared = min(
                obj['x1'], obj['z1'],
                habitacion['ancho'] - obj['x2'],
                habitacion['profundidad'] - obj['z2']
            )
            puntuacion -= dist_pared * 2

    for nombre1, nombre2 in reglas_adyacencia:
        obj1 = next((o for o in objetos if o['nombre'] == nombre1), None)
        obj2 = next((o for o in objetos if o['nombre'] == nombre2), None)
        if obj1 and obj2:
            distancia = calcular_distancia((obj1['cx'], obj1['cz']),
                                           (obj2['cx'], obj2['cz']))
            if distancia <= 1:
                puntuacion += 150
            else:
                puntuacion -= distancia * 10

    return puntuacion
