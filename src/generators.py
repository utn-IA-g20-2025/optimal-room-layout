import random

from src import values

mueble_id_counter = 0
global habitacion

def get_lista_tomas():
    cantidad_tomas = random.randint(2, 10),
    lista_tomas = dict
    for _ in cantidad_tomas:
        lista_tomas.update({
            'x': random.randint(0, habitacion["ancho"]),
            'y': random.randint(0, habitacion["profundidad"])
        })


def get_reglas_adyacencia():
    # TODO reglas_adyacencia: lista de tuplas con nombres de objetos que deben estar juntos.
    pass


def generar_habitacion():
    hab = {
        "ancho": random.randint(200, 1000),
        "profundidad": random.randint(200, 1000),
        "tomas": get_lista_tomas(),
        "reglas_adyacencia": get_reglas_adyacencia()
    }
    return hab



def generar_mueble(hab):
    global mueble_id_counter
    mueble = {
        "id": mueble_id_counter,
        "tipo": random.choice(values.TIPOS),
        "ancho": random.randint(50, 100),
        "profundidad": random.randint(50, 100),
        "x":  random.randint(0, hab["ancho"]),
        "y": random.randint(0, hab["profundidad"]),
        "rot": random.randint(0, 90),
        "requiere_toma": bool(random.getrandbits(1)),
        "debe_ir_a_pared": bool(random.getrandbits(1))
    }
    mueble_id_counter += 1
    return mueble

def generar_set_nuebles(hab):
    return [generar_mueble(hab) for _ in range(7)]  # Se puede tomar de un archivo csv
