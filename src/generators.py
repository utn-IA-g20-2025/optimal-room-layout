import random

from values import MUEBLES, HABITACION

def generar_mueble(info_mueble):
    return {
        "id": info_mueble["nombre"],
        "ancho": info_mueble["ancho"],
        "profundidad": info_mueble["profundidad"],
        "necesita_toma": info_mueble["necesita_toma"],
        "lado_frontal": info_mueble["lado_frontal"],
        "margen_a": info_mueble["margen_a"],
        "margen_b": info_mueble["margen_b"],
        "margen_c": info_mueble["margen_c"],
        "margen_d": info_mueble["margen_d"],
        "x": random.randint(0, HABITACION["ancho"]),
        "y": random.randint(0, HABITACION["profundidad"]),
        "rot": random.choice([0, 90, 180, 270])
    }

# individuo = lista de muebles en ubicaciones al azar
def generar_set_muebles():
    return [generar_mueble(info_mueble) for info_mueble in MUEBLES]
