import math

from values import HABITACION


def calcular_distancia(coordenadas1, coordenadas2):
    return math.sqrt(
        (coordenadas1[0] - coordenadas2[0]) ** 2 +
        (coordenadas1[1] - coordenadas2[1]) ** 2
    )


def calcular_bounding_box(mueble):
    """
    Calcula el bounding box de un objeto considerando su rotacion.
    Args:
        mueble: objeto sobre el que se quiere calcular su bounding box
    Returns:
        tuple: (x1, y1, x2, y2) representando el bounding box.
    """
    x, y, ancho, profundidad, rot = (
        mueble["x"],
        mueble["y"],
        mueble["ancho"],
        mueble["profundidad"],
        mueble["rot"]
    )
    if rot in (0, 180):
        return x + ancho / 2, y + profundidad / 2, x - ancho / 2, y - profundidad / 2
    else: # 90, 270
        return x + profundidad / 2, y + ancho / 2, x - profundidad / 2, y - ancho / 2


def calcular_distancia_a_pared(mueble):
    """
    Calcula la distancia mínima de un objeto a la pared más cercana.
    Args:
        mueble: objeto sobre el que se quiere hacer el calculo
    Returns:
        float: La distancia mínima a la pared.
    """
    bbox = calcular_bounding_box(mueble)
    return min(
        bbox[0], bbox[1],
        HABITACION["ancho"] - bbox[2],
        HABITACION["profundidad"] - bbox[3]
    )


def calcular_distancia_a_toma(mueble):
    """
    Calcula la distancia mínima de un objeto a la toma de corriente más cercana.
    Args:
        mueble: objeto sobre el que se quiere hacer el calculo
    Returns:
        float: La distancia mínima a la toma de corriente.
    """
    return min([
        calcular_distancia((mueble["x"], mueble["y"]), (toma["x"], toma["y"]))
        for toma in HABITACION["tomas"]
    ])


def calcular_solapamiento(bbox1, bbox2):
    """
    Calcula si dos bounding boxes se solapan.
    Args:
        bbox1: Bounding box del primer objeto (x1, y1, x2, y2).
        bbox2: Bounding box del segundo objeto (x1, y1, x2, y2).
    Returns:
        bool: True si los bounding boxes se solapan, False en caso contrario.
    """
    # TODO: faltaria tener en cuenta los margenes
    return not (
            bbox1[2] <= bbox2[0] or bbox2[2] <= bbox1[0] or
            bbox1[3] <= bbox2[1] or bbox2[3] <= bbox1[1]
    )


def calcular_penalizacion_adyacencia(mueble1, mueble2):
    """
    Calcula la penalización o recompensa por la adyacencia entre dos objetos.
    Args:
        mueble1, mueble2: par de objetos adyacentes
    Returns:
        float: La penalización o recompensa por la adyacencia.
    """
    distancia = calcular_distancia(
        (mueble1["x"], mueble1["y"]),
        (mueble2["x"], mueble2["y"])
    )
    if distancia <= 1:
        return 150
    return -distancia * 10


def calcular_penalizacion_solapamiento(mueble1, mueble2):
    """
    Calcula la penalización por solapamiento entre dos objetos.
    Args:
        mueble1: Primer objeto
        mueble2: Segundo objeto
    Returns:
        float: La penalización por solapamiento.
    """
    bbox1 = calcular_bounding_box(mueble1)
    bbox2 = calcular_bounding_box(mueble2)
    if calcular_solapamiento(bbox1, bbox2):
        return 300
    return 0


def calcular_penalizacion_toma(mueble):
    """
    Calcula la penalización por la distancia a la toma de corriente más cercana.
    Args:
        mueble: Objeto sobre el que se quiere calcular la penalizacion, si es que requiere un toma
    Returns:
        float: La penalización por la distancia a la toma de corriente.
    """
    if mueble['requiere_toma']:
        dist_min = calcular_distancia_a_toma(mueble)
        return dist_min * 5
    return 0


def calcular_penalizacion_pared(mueble):
    """
    Calcula la penalización por la distancia a la pared más cercana.
    Args:
        mueble: Objeto sobre el que se quiere calcular la penalizacion, teniendo en cuenta su cara frontal si aplica
    Returns:
        float: La penalización por la distancia a la pared.
    """
    # TODO: esta condicion debería depender de si el mueble tiene cara frontal, y si esa cara esta apuntando hacia la pared o no
    debe_ir_a_pared = False
    if debe_ir_a_pared:
        dist_pared = calcular_distancia_a_pared(mueble)
        return dist_pared * 2
    return 0


def fitness(muebles):
    """
    Calcula la puntuación de aptitud para una disposición de muebles en la habitación.
    Args:
        muebles: Un individuo. Lista de muebles/electrodomésticos, cada uno es un dict con estas keys:
            - nombre
            - ancho
            - profundidad
            - requiere_toma: si requiere estar cercano a un toma corriente (True/False)
            - lado_frontal: cara que no debe ir contra la pared
            - margen_a, margen_b, margen_c, margen_d: margenes de espacio requerido a su alrededor
            - x: posición en x
            - y: posición en y
            - rot: rotación en grados. valores posibles: 0, 90, 180, 270
    Returns:
        float: La puntuación de aptitud para la disposición de muebles.
    """
    puntuacion = 1000  # base

    for i in range(len(muebles)):
        for j in range(i + 1, len(muebles)):
            puntuacion -= calcular_penalizacion_solapamiento(muebles[i], muebles[j])

    for mueble in muebles:
        puntuacion -= calcular_penalizacion_toma(mueble)
        puntuacion -= calcular_penalizacion_pared(mueble)

    for nombre1, nombre2 in HABITACION["reglas_adyacencia"]:
        mueble1 = next((mueble for mueble in muebles if mueble['nombre'] == nombre1), None)
        mueble2 = next((mueble for mueble in muebles if mueble['nombre'] == nombre2), None)
        if mueble1 and mueble2:
            puntuacion += calcular_penalizacion_adyacencia(mueble1, mueble2)

    return puntuacion
