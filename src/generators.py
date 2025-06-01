import random
from math import floor

from src.values import MUEBLES, HABITACION

def generar_mueble(info_mueble):
    ancho_habitacion, profundidad_habitacion = (
        HABITACION["ancho"],
        HABITACION["profundidad"]
    )
    mitad_ancho, mitad_profundidad = (
        floor(info_mueble["ancho"] / 2),
        floor(info_mueble["profundidad"] / 2)
    )
    margen_a, margen_b, margen_c, margen_d = (
        info_mueble['margen_a'], 
        info_mueble['margen_b'], 
        info_mueble['margen_c'], 
        info_mueble['margen_d']
    )
    rotacion = random.choice([0, 90, 180, 270])
    if rotacion == 0:
        x_min = 0 + mitad_ancho + margen_d
        x_max = ancho_habitacion - mitad_ancho - margen_b
        y_min = 0 + mitad_profundidad + margen_c
        y_max = profundidad_habitacion - mitad_profundidad - margen_a
    elif rotacion == 90:
        x_min = 0 + mitad_profundidad + margen_a
        x_max = ancho_habitacion - mitad_profundidad - margen_c
        y_min = 0 + mitad_ancho + margen_d
        y_max = profundidad_habitacion - mitad_ancho - margen_b
    elif rotacion == 180:
        x_min = 0 + mitad_ancho + margen_b
        x_max = ancho_habitacion - mitad_ancho - margen_d
        y_min = 0 + mitad_profundidad + margen_a
        y_max = profundidad_habitacion - mitad_profundidad - margen_c
    else: #270
        x_min = 0 + mitad_profundidad + margen_c
        y_min = 0 + mitad_ancho + margen_b
        x_max = ancho_habitacion - mitad_profundidad - margen_a
        y_max = profundidad_habitacion - mitad_ancho - margen_d

    return {
        "nombre": info_mueble["nombre"],
        "ancho": info_mueble["ancho"],
        "profundidad": info_mueble["profundidad"],
        "requiere_toma": info_mueble["requiere_toma"],
        "debe_ir_a_pared": info_mueble["debe_ir_a_pared"],
        "lado_frontal": info_mueble["lado_frontal"],
        "margen_a": margen_a,
        "margen_b": margen_b,
        "margen_c": margen_c,
        "margen_d": margen_d,
        "x": random.randint(x_min, x_max),
        "y": random.randint(y_min, y_max),
        "rot": rotacion
    }

# individuo = lista de muebles en ubicaciones al azar
def generar_set_muebles():
    return [generar_mueble(info_mueble) for info_mueble in MUEBLES]
