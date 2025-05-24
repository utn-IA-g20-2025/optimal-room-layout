import random

from src import values

mueble_id_counter = 0
global habitacion

def getListaTomas():
    cantidad_tomas = random.randint(2, 10),
    lista_tomas = dict
    for toma in cantidad_tomas:
        lista_tomas.update({
            'x': random.randint(0, habitacion["ancho"]),
            'y': random.randint(0, habitacion["profundidad"])
        })


def get_reglas_adyacencia():
    pass


def generar_habitacion():
    habitacion = {
        "ancho": random.randint(200, 1000),
        "profundidad": random.randint(200, 1000),
        "tomas": getListaTomas(),
        "reglas_adyacencia": get_reglas_adyacencia()
    }
    return habitacion


habitacion= generar_habitacion()

def generar_mueble():
    global mueble_id_counter
    musico = {
        "id": mueble_id_counter,
        "nombre": random.choice(values.TIPOS),
        "ancho": random.randint(50, 100),
        "profundidad": random.randint(50, 100),
        "x":  random.randint(0, habitacion["ancho"]),
        "y": random.randint(0, habitacion["profundidad"]),
        "rot": random.randint(0, 90),
        "requiere_toma": bool(random.getrandbits(1)),
        "debe_ir_a_pared": bool(random.getrandbits(1)),
        "ambicion": random.randint(0, 100),
        "ubicacion_geografica": random.choice(values.UBICACIONES)
    }
    mueble_id_counter += 1
    return musico

def generar_set_nuebles():
    return [generar_mueble() for _ in range(5)]  # Se puede tomar de un archivo csv
