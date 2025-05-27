import random

from src import values

mueble_id_counter = 0


def get_lista_tomas(ancho, prof):
    cantidad_tomas = random.randint(2, 10)
    lista_tomas = []
    for _ in range(cantidad_tomas):
        lista_tomas.append({
            "x": random.randint(0, ancho),
            "y": random.randint(0, prof)
        })
    return lista_tomas


def get_reglas_adyacencia():
    # TODO reglas_adyacencia: lista de tuplas con nombres de objetos que deben estar juntos.
    pass


def generar_habitacion():
    values.HABITACION = {}
    ancho = random.randint(200, 1000)
    prof = random.randint(200, 1000)
    lista_tomas = get_lista_tomas(ancho, prof)
    habitacion = {'ancho': ancho,
                  'profundidad': prof,
                  'tomas': lista_tomas,
                  'reglas_adyacencia': get_reglas_adyacencia()
                  }
    values.HABITACION = habitacion
    return habitacion


def generar_mueble():
    global mueble_id_counter
    mueble = {
        "id": mueble_id_counter,
        "tipo": random.choice(values.TIPOS),
        "ancho": random.randint(50, 100),
        "profundidad": random.randint(50, 100),
        "x": random.randint(0, values.HABITACION["ancho"]),
        "y": random.randint(0, values.HABITACION["profundidad"]),
        "rot": random.randint(0, 90),
        "requiere_toma": bool(random.getrandbits(1)),
        "debe_ir_a_pared": bool(random.getrandbits(1))
    }
    mueble_id_counter += 1
    return mueble


def generar_set_muebles():
    return [generar_mueble() for _ in range(values.CANT_MAX_MUEBLES)]  # Se puede tomar de un archivo csv
