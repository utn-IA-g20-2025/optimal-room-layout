import math

from src import values
from values import HABITACION


def calcular_distancia(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def calcular_bounding_box(x, y, ancho, profundidad, rot):
    """
    Calcula el bounding box de un objeto rotado.
    Args:
        x: Coordenada x del centro del objeto.
        y: Coordenada y del centro del objeto.
        ancho: Ancho del objeto.
        profundidad: Profundidad del objeto.
        rot: Rotación en grados.
    Returns:
        tuple: (x1, y1, x2, y2) representando el bounding box.
    """
    rad = math.radians(rot)
    cos_rot = math.cos(rad)
    sin_rot = math.sin(rad)
    half_w = ancho / 2
    half_d = profundidad / 2
    dx = half_w * cos_rot - half_d * sin_rot
    dy = half_w * sin_rot + half_d * cos_rot
    return (x - dx, y - dy, x + dx, y + dy)


def calcular_distancia_a_pared(x, y, ancho, profundidad, rot, ancho_habitacion, profundidad_habitacion):
    """
    Calcula la distancia mínima de un objeto a la pared más cercana.
    Args:
        x: Coordenada x del centro del objeto.
        y: Coordenada y del centro del objeto.
        ancho: Ancho del objeto.
        profundidad: Profundidad del objeto.
        rot: Rotación en grados.
        ancho_habitacion: Ancho de la habitación.
        profundidad_habitacion: Profundidad de la habitación.
    Returns:
        float: La distancia mínima a la pared.
    """
    bbox = calcular_bounding_box(x, y, ancho, profundidad, rot)
    return min(
        bbox[0], bbox[1],
        ancho_habitacion - bbox[2],
        profundidad_habitacion - bbox[3]
    )


def calcular_distancia_a_toma(x, y, tomas):
    """
    Calcula la distancia mínima de un objeto a la toma de corriente más cercana.
    Args:
        x: Coordenada x del centro del objeto.
        y: Coordenada y del centro del objeto.
        tomas: Lista de coordenadas (x, y) de las tomas de corriente.
    Returns:
        float: La distancia mínima a la toma de corriente.
    """
    return min([calcular_distancia((x, y), list(toma.values())) for toma in tomas])


def calcular_distancia_entre_objetos(obj1, obj2):
    """
    Calcula la distancia entre dos objetos.
    Args:
        obj1: Primer objeto con keys 'cx' y 'cz'.
        obj2: Segundo objeto con keys 'cx' y 'cz'.
    Returns:
        float: La distancia entre los centros de los objetos.
    """
    return calcular_distancia((obj1['cx'], obj1['cz']), (obj2['cx'], obj2['cz']))


def calcular_solapamiento(bbox1, bbox2):
    """
    Calcula si dos bounding boxes se solapan.
    Args:
        bbox1: Bounding box del primer objeto (x1, y1, x2, y2).
        bbox2: Bounding box del segundo objeto (x1, y1, x2, y2).
    Returns:
        bool: True si los bounding boxes se solapan, False en caso contrario.
    """
    return not (
            bbox1[2] <= bbox2[0] or bbox2[2] <= bbox1[0] or
            bbox1[3] <= bbox2[1] or bbox2[3] <= bbox1[1]
    )


def calcular_penalizacion_fuera_de_limites(x, y, ancho, profundidad, ancho_habitacion, profundidad_habitacion):
    """
    Calcula la penalización por estar fuera de los límites de la habitación.
    Args:
        x: Coordenada x del centro del objeto.
        y: Coordenada y del centro del objeto.
        ancho: Ancho del objeto.
        profundidad: Profundidad del objeto.
        ancho_habitacion: Ancho de la habitación.
        profundidad_habitacion: Profundidad de la habitación.
    Returns:
        float: La penalización por estar fuera de los límites.
    """
    if (x < 0 or y < 0 or
            x + ancho > ancho_habitacion or
            y + profundidad > profundidad_habitacion):
        return 200
    return 0


def calcular_penalizacion_adyacencia(obj1, obj2):
    """
    Calcula la penalización o recompensa por la adyacencia entre dos objetos.
    Args:
        obj1: Primer objeto con keys 'cx' y 'cz'.
        obj2: Segundo objeto con keys 'cx' y 'cz'.
    Returns:
        float: La penalización o recompensa por la adyacencia.
    """
    distancia = calcular_distancia_entre_objetos(obj1, obj2)
    if distancia <= 1:
        return 150
    return -distancia * 10


def calcular_penalizacion_solapamiento(bbox1, bbox2):
    """
    Calcula la penalización por solapamiento entre dos objetos.
    Args:
        bbox1: Bounding box del primer objeto (x1, y1, x2, y2).
        bbox2: Bounding box del segundo objeto (x1, y1, x2, y2).
    Returns:
        float: La penalización por solapamiento.
    """
    if calcular_solapamiento(bbox1, bbox2):
        return 300
    return 0


def calcular_penalizacion_toma(obj, tomas):
    """
    Calcula la penalización por la distancia a la toma de corriente más cercana.
    Args:
        obj: Objeto con keys 'cx' y 'cz'.
        tomas: Lista de coordenadas (x, y) de las tomas de corriente.
    Returns:
        float: La penalización por la distancia a la toma de corriente.
    """
    if obj['requiere_toma']:
        dist_min = calcular_distancia_a_toma(obj['cx'], obj['cz'], tomas)
        return dist_min * 5
    return 0


def calcular_penalizacion_pared(obj, rot, ancho_habitacion, profundidad_habitacion):
    """
    Calcula la penalización por la distancia a la pared más cercana.
    Args:
        obj: Objeto con keys 'cx', 'cz', 'x1', 'z1', 'x2', 'z2'.
        rot: Rotación del objeto.
        ancho_habitacion: Ancho de la habitación.
        profundidad_habitacion: Profundidad de la habitación.
    Returns:
        float: La penalización por la distancia a la pared.
    """
    if obj['debe_ir_a_pared']:
        dist_pared = calcular_distancia_a_pared(obj['cx'], obj['cz'], obj['x2'] - obj['x1'], obj['z2'] - obj['z1'], rot, ancho_habitacion, profundidad_habitacion)
        return dist_pared * 2
    return 0


def fitness(muebles):
    """
    Calcula la puntuación de aptitud para una disposición de muebles en la habitación.
    Args:
        muebles: Lista de muebles/electrodomésticos, cada uno como un dict con keys:
            - 'nombre'
            - 'ancho', 'profundidad'
            - 'x', 'z' (posición)
            - 'rot' (rotación en grados: 0 o 90)
        reglas_adyacencia: Lista de tuplas con nombres de objetos que deben estar juntos.
    Returns:
        float: La puntuación de aptitud para la disposición de muebles.
    """
    puntuacion = 1000  # base

    objetos = []

    for mueble in muebles:
        if mueble['rot'] == 90:
            w, d = mueble['profundidad'], mueble['ancho']
        else:
            w, d = mueble['ancho'], mueble['profundidad']

        x, z = mueble['x'], mueble['y']

        puntuacion -= calcular_penalizacion_fuera_de_limites(x, z, w, d, HABITACION['ancho'], HABITACION['profundidad'])

        objetos.append({
            'tipo': mueble['tipo'],
            'x1': x, 'z1': z,
            'x2': x + w, 'z2': z + d,
            'cx': x + w / 2, 'cz': z + d / 2,
            'requiere_toma': mueble.get('requiere_toma', False),
            'debe_ir_a_pared': mueble.get('debe_ir_a_pared', False)
        })

    for i in range(len(objetos)):
        for j in range(i + 1, len(objetos)):
            o1, o2 = objetos[i], objetos[j]
            # Usar calcular_bounding_box para detectar solapamiento
            bbox1 = calcular_bounding_box(o1['cx'], o1['cz'], o1['x2'] - o1['x1'], o1['z2'] - o1['z1'], muebles[i]['rot'])
            bbox2 = calcular_bounding_box(o2['cx'], o2['cz'], o2['x2'] - o2['x1'], o2['z2'] - o2['z1'], muebles[j]['rot'])
            puntuacion -= calcular_penalizacion_solapamiento(bbox1, bbox2)

    tomas = HABITACION["tomas"]

    for obj in objetos:
        puntuacion -= calcular_penalizacion_toma(obj, tomas)

    for idx, obj in enumerate(objetos):
        puntuacion -= calcular_penalizacion_pared(obj, muebles[idx]['rot'], HABITACION['ancho'], HABITACION['profundidad'])

    for nombre1, nombre2 in HABITACION["reglas_adyacencia"]:
        obj1 = next((o for o in objetos if o['nombre'] == nombre1), None)
        obj2 = next((o for o in objetos if o['nombre'] == nombre2), None)
        if obj1 and obj2:
            puntuacion += calcular_penalizacion_adyacencia(obj1, obj2)

    return puntuacion,
