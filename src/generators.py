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
    ancho = random.randint(200, 1000)
    prof = random.randint(200, 1000)
    lista_tomas = get_lista_tomas(ancho, prof)
    lista_muebles = generar_set_muebles(ancho, prof)
    return {'ancho': ancho, 'profundidad': prof, 'tomas': lista_tomas,'muebles': lista_muebles, 'reglas_adyacencia': get_reglas_adyacencia()}



def generar_mueble(ancho, prof):
    global mueble_id_counter
    mueble = {
        "id": mueble_id_counter,
        "tipo": random.choice(values.TIPOS),
        "ancho": random.randint(50, 100),
        "profundidad": random.randint(50, 100),
        "x":  random.randint(0, ancho),
        "y": random.randint(0, prof),
        "rot": random.randint(0, 90),
        "requiere_toma": bool(random.getrandbits(1)),
        "debe_ir_a_pared": bool(random.getrandbits(1))
    }
    mueble_id_counter += 1
    return mueble

def generar_set_muebles(ancho, prof):
    return [generar_mueble(ancho, prof) for _ in range(7)]  # Se puede tomar de un archivo csv
