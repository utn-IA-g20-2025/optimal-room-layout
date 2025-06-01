import math
from itertools import combinations

from src.values import HABITACION

PUNTUACION_INICIAL = 1000
PENALIZACION_PARED = 200
RECOMPENSA_PARED = 100
PENALIZACION_LADO_FRONTAL = 300
RECOMPENSA_LADO_FRONTAL = -100 # recompensa = este valor / distancia
PENALIZACION_ENFRENTAMIENTO_DURO = 80
PENALIZACION_ENFRENTAMIENTO_DEBIL = 50
RECOMPENSA_ENFRENTAMIENTO = 20000
PENALIZACION_TOMA = 10  # penalización = distancia * este valor
RECOMPENSA_TOMA = 5
PENALIZACION_ADYACENCIA = 50  # penalización = distancia * este valor
RECOMPENSA_ADYACENCIA = 25
PENALIZACION_SOLAPAMIENTO = 5
RECOMPENSA_SOLAPAMIENTO = 2
PENALIZACION_SOLAPAMIENTO_DURO = -9999999

def calcular_distancia(coordenadas1, coordenadas2):
    return math.sqrt(
        (coordenadas1[0] - coordenadas2[0]) ** 2 +
        (coordenadas1[1] - coordenadas2[1]) ** 2
    )

def calcular_distancia_minima(bbox1, bbox2):
    """
    Calcula la distancia mínima entre dos bounding boxes.
    """
    if se_solapan(bbox1, bbox2):
        return 0

    x1_min, y1_min, x1_max, y1_max = bbox1
    x2_min, y2_min, x2_max, y2_max = bbox2

    # Distancia horizontal
    if x1_max < x2_min:
        dx = x2_min - x1_max
    else:
        dx = x1_min - x2_max

    # Distancia vertical
    if y1_max < y2_min:
        dy = y2_min - y1_max
    else:
        dy = y1_min - y2_max

    return math.sqrt(dx ** 2 + dy ** 2)

def calcular_bounding_box(mueble):
    """
    Calcula el bounding box de un objeto considerando su rotacion.
    Args:
        mueble: objeto sobre el que se quiere calcular su bounding box
    Returns:
        tuple: (x1, y1, x2, y2) representando el bounding box.
    """
    x, y, ancho, profundidad, rot, ma, mb, mc, md = (
        mueble["x"],
        mueble["y"],
        mueble["ancho"],
        mueble["profundidad"],
        mueble["rot"],
        mueble["margen_a"],
        mueble["margen_b"],
        mueble["margen_c"],
        mueble["margen_d"]
    )
    mitad_ancho = ancho / 2
    mitad_prof = profundidad / 2
    if rot == 0:
        return x - mitad_ancho - md, y - mitad_prof - mc, x + mitad_ancho + mb, y + mitad_prof + ma
    elif rot == 90:
        return x - mitad_prof - ma, y - mitad_ancho - md, x + mitad_prof + mc, y + mitad_ancho + mb
    elif rot == 180:
        return x - mitad_ancho - mb, y - mitad_prof - ma, x + mitad_ancho + md, y + mitad_prof + mc
    else: #270
        return x - mitad_prof - mc, y - mitad_ancho - mb, x + mitad_prof + ma, y + mitad_ancho + md


def calcular_bounding_box_sin_margenes(mueble):
    mueble_sin_margenes = mueble.copy()
    mueble_sin_margenes.update({
        "margen_a": 0,
        "margen_b": 0,
        "margen_c": 0,
        "margen_d": 0
    })
    return calcular_bounding_box(mueble_sin_margenes)

def calcular_distancia_a_pared(mueble):
    """
    Calcula la distancia mínima de un objeto a la pared más cercana.
    Args:
        mueble: objeto sobre el que se quiere hacer el calculo
    Returns:
        float: La distancia mínima a la pared.
    """
    bbox = calcular_bounding_box(mueble)
    """
    if mueble["lado_frontal"]:
        sentido = sentido_por_lado_segun_rotacion[mueble["rot"]][mueble["lado_frontal"]]
        if sentido == 0:
            return bbox[0]
        elif sentido == 90:
            return bbox[1]
        elif sentido == 180:
            return HABITACION["ancho"] - bbox[2]
        else:
            return HABITACION["profundidad"] - bbox[3]
    else:
    """
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


def se_solapan(bbox1, bbox2):
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

def calcular_penalizacion_fuera_de_limites(mueble):
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
    bbox = calcular_bounding_box(mueble)
    if (bbox[0] < 0 or
        bbox[1] < 0 or
        bbox[2] > HABITACION["ancho"] or
        bbox[3] > HABITACION["profundidad"]):
        return 200
    return 0

def calcular_penalizacion_adyacencia(mueble1, mueble2):
    """
    Calcula la penalización o recompensa por la adyacencia entre dos objetos.
    Args:
        mueble1, mueble2: par de objetos adyacentes
    Returns:
        float: La penalización o recompensa por la adyacencia.
    """
    bbox1 = calcular_bounding_box(mueble1)
    bbox2 = calcular_bounding_box(mueble2)

    #if se_solapan(bbox1, bbox2):
    #    return 100

    distancia = calcular_distancia_minima(bbox1, bbox2)
    if distancia <= 1:
        return RECOMPENSA_ADYACENCIA # recompensa
    return distancia * PENALIZACION_ADYACENCIA


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
    if se_solapan(bbox1, bbox2):
        return PENALIZACION_SOLAPAMIENTO
    return RECOMPENSA_SOLAPAMIENTO


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
        return dist_min * PENALIZACION_TOMA
    return RECOMPENSA_TOMA


def calcular_penalizacion_lado_frontal(mueble):
    lado_frontal = mueble['lado_frontal']
    if lado_frontal and mueble["debe_ir_a_pared"]:
        sentido = sentido_por_lado_segun_rotacion[mueble["rot"]][lado_frontal]
        bbox = calcular_bounding_box(mueble)
        if sentido == 0:
            distancia_a_pared_respetando_lado_frontal = bbox[0]
        elif sentido == 90:
            distancia_a_pared_respetando_lado_frontal = bbox[1]
        elif sentido == 180:
            distancia_a_pared_respetando_lado_frontal = HABITACION["ancho"] - bbox[2]
        else:
            distancia_a_pared_respetando_lado_frontal = HABITACION["profundidad"] - bbox[3]

        if calcular_distancia_a_pared(mueble) < distancia_a_pared_respetando_lado_frontal: # si esto pasa, el mueble no esta apuntando al lado correcto
            return PENALIZACION_LADO_FRONTAL
        else:
            return RECOMPENSA_LADO_FRONTAL/distancia_a_pared_respetando_lado_frontal
    else:
        return 0

def calcular_penalizacion_pared(mueble):
    """
    Calcula la penalización por la distancia a la pared más cercana.
    Args:
        mueble: Objeto sobre el que se quiere calcular la penalizacion, teniendo en cuenta su cara frontal si aplica
    Returns:
        float: La penalización por la distancia a la pared.
    """
    if mueble["debe_ir_a_pared"]:
        dist_pared = calcular_distancia_a_pared(mueble)
        if dist_pared > 0:
            return PENALIZACION_PARED
        else:
            return RECOMPENSA_PARED
    return 0

"""
Ej, si el objeto esta rotado a 0°:
          (90°)
            A
         +----+
(180°) D |    | B (0°)
         +----+
            C       
          (270°)
          
Si el objeto esta rotado a 90°:
          (90°)
            B
         +----+
(180°) A |    | C (0°)
         +----+
            D       
          (270°)
          
etc
"""
sentido_por_lado_segun_rotacion = {
    0: {"a": 90, "b": 0, "c": 270, "d": 180},
    90: {"b": 90, "c": 0, "d": 270, "a": 180},
    180: {"c": 90, "d": 0, "a": 270, "b": 180},
    270: {"d": 90, "a": 0, "b": 270, "c": 180},
}

def calcular_penalizacion_enfrentamiento(mueble1, mueble2):
    sentido_lado_frontal1 = sentido_por_lado_segun_rotacion[mueble1["rot"]][mueble1["lado_frontal"]]
    sentido_lado_frontal2 = sentido_por_lado_segun_rotacion[mueble2["rot"]][mueble2["lado_frontal"]]
    lados_son_opuestos = abs(sentido_lado_frontal1 - sentido_lado_frontal2) == 180
    if lados_son_opuestos:
        (x1_min, y1_min, x1_max, y1_max) = calcular_bounding_box(mueble1)
        (x2_min, y2_min, x2_max, y2_max) = calcular_bounding_box(mueble2)
        if sentido_lado_frontal1 in (0, 180):
            if y1_max - y1_min <= y2_max - y2_min:
                estan_enfrentados = y1_min >= y2_min and y1_max <= y2_max
            else:
                estan_enfrentados = y2_min >= y1_min and y2_max <= y1_max
        else:
            if x1_max - x1_min <= x2_max - x2_min:
                estan_enfrentados = x1_min >= x2_min and x1_max <= x2_max
            else:
                estan_enfrentados = x2_min >= x1_min and x2_max <= x1_max

        if estan_enfrentados:
            return RECOMPENSA_ENFRENTAMIENTO
        else:
            return PENALIZACION_ENFRENTAMIENTO_DEBIL
    else:
        return PENALIZACION_ENFRENTAMIENTO_DURO

def encontrar_mueble(modelo_mueble, muebles_en_habitacion):
    return next((mueble for mueble in muebles_en_habitacion if mueble['nombre'] == modelo_mueble["nombre"]), None)

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

    for (mueble1, mueble2) in combinations(muebles, 2):
        if se_solapan(
                calcular_bounding_box_sin_margenes(mueble1),
                calcular_bounding_box_sin_margenes(mueble2)
        ):
            return PENALIZACION_SOLAPAMIENTO_DURO,

    puntuacion = PUNTUACION_INICIAL

    for (mueble1, mueble2) in combinations(muebles, 2):
        puntuacion -= calcular_penalizacion_solapamiento(mueble1, mueble2)

    for mueble in muebles:
        puntuacion -= calcular_penalizacion_toma(mueble)
        puntuacion -= calcular_penalizacion_pared(mueble)
        puntuacion -= calcular_penalizacion_lado_frontal(mueble)
        #puntuacion -= calcular_penalizacion_fuera_de_limites(mueble)

    for regla in HABITACION["reglas_adyacencia"]:
        mueble1 = encontrar_mueble(regla[0], muebles)
        mueble2 = encontrar_mueble(regla[1], muebles)
        if mueble1 and mueble2:
            puntuacion -= calcular_penalizacion_adyacencia(mueble1, mueble2)

    for regla in HABITACION["reglas_enfrentamiento"]:
        mueble1 = encontrar_mueble(regla[0], muebles)
        mueble2 = encontrar_mueble(regla[1], muebles)
        if mueble1 and mueble2 and mueble1["lado_frontal"] and mueble2["lado_frontal"]:
            puntuacion -= calcular_penalizacion_enfrentamiento(mueble1, mueble2)

    return puntuacion,
