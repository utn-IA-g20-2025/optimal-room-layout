"""
                                     90°
 y ^     ancho                       ^                       A
   |   +--+                          |                     +--+            A=C
   |   |  |  prof           180° <-     -> 0°            D |  | B          B=D
   |   +--+                          |                     +--+
   +-----------> x                   v                       C
                                    270°
"""

"""
- Cada objeto tiene 4 caras, A, B, C y D. Donde A mide lo mismo que C (w = width), y B lo mismo que D (l = length).
- De esas 4, habría que especificar si tiene alguna cara frontal (cara que no puede ir contra una pared, ej la pantalla de la TV), 
    si todas las caras podrían potencialmente ir contra una pared, se deja en None (ej la mesa, que se puede poner contra una pared, o no). 
- Los objetos que requieren electricidad deberían colocarse a una proximidad de x (a definir) cm de un toma
- Los objetos deberían tener margenes, es decir, mas alla de sus dimensiones, pueden requerir espacio adicional a su alrededor 
    (si una cara puede ir contra la pared, el margen de esa cara no se debería tener en cuenta en la f de aptitud)
"""

# Muebles disponibles
mesa_con_sillas = {
    "nombre": "Mesa con sillas",
    "ancho": 95,
    "profundidad": 160,
    "requiere_toma": False,
    "debe_ir_a_pared": False,
    "lado_frontal": "d",
    "margen_a": 20,
    "margen_b": 20,
    "margen_c": 20,
    "margen_d": 20
}

cama = {
    "nombre": "Cama",
    "ancho": 140,
    "profundidad": 190,
    "requiere_toma": False,
    "debe_ir_a_pared": True,
    "lado_frontal": None,
    "margen_a": 25,
    "margen_b": 25,
    "margen_c": 25,
    "margen_d": 25
}

tv = {
    "nombre": "TV",
    "ancho": 145,
    "profundidad": 8,
    "requiere_toma": True,
    "debe_ir_a_pared": True,
    "lado_frontal": "c",
    "margen_a": 3,
    "margen_b": 10,
    "margen_c": 80,
    "margen_d": 10
}

biblioteca = {
    "nombre": "Biblioteca",
    "ancho": 60,
    "profundidad": 40,
    "requiere_toma": False,
    "debe_ir_a_pared": True,
    "lado_frontal": "c",
    "margen_a": 5,
    "margen_b": 5,
    "margen_c": 40,
    "margen_d": 5
}

sillon = {
    "nombre": "Sillón",
    "ancho": 180,
    "profundidad": 80,
    "requiere_toma": False,
    "debe_ir_a_pared": False,
    "lado_frontal": "a",
    "margen_a": 60,
    "margen_b": 0,
    "margen_c": 0,
    "margen_d": 0
}

escritorio = {
    "nombre": "Escritorio",
    "ancho": 120,
    "profundidad": 60,
    "requiere_toma": True,
    "debe_ir_a_pared": False,
    "lado_frontal": "a",
    "margen_a": 60,
    "margen_b": 5,
    "margen_c": 5,
    "margen_d": 5
}

lavarropas = {
    "nombre": "Lavarropas",
    "ancho": 54,
    "profundidad": 54,
    "requiere_toma": True,
    "debe_ir_a_pared": True,
    "lado_frontal": "a",
    "margen_a": 40,
    "margen_b": 10,
    "margen_c": 10,
    "margen_d": 10
}

heladera = {
    "nombre": "Heladera",
    "ancho": 60,
    "profundidad": 64,
    "requiere_toma": True,
    "debe_ir_a_pared": True,
    "lado_frontal": "c",
    "margen_a": 15,
    "margen_b": 10,
    "margen_c": 60,
    "margen_d": 10
}

cocina = {
    "nombre": "Cocina",
    "ancho": 58,
    "profundidad": 62,
    "requiere_toma": True,
    "debe_ir_a_pared": True,
    "lado_frontal": "a",
    "margen_a": 15,
    "margen_b": 3,
    "margen_c": 0,
    "margen_d": 3
}

lampara = {
    "nombre": "Lampara",
    "ancho": 30,
    "profundidad": 30,
    "requiere_toma": True,
    "debe_ir_a_pared": False,
    "lado_frontal": None,
    "margen_a": 5,
    "margen_b": 5,
    "margen_c": 5,
    "margen_d": 5
}

cuadro = {
    "nombre": "Cuadro",
    "ancho": 50,
    "profundidad": 3,
    "requiere_toma": True,
    "debe_ir_a_pared": True,
    "lado_frontal": "c",
    "margen_a": 0,
    "margen_b": 0,
    "margen_c": 20,
    "margen_d": 0
}

habitacion_1 = {
    "muebles": [ mesa_con_sillas, tv, biblioteca, sillon, escritorio, lampara, cuadro ],
    "ancho": 400,
    "profundidad": 350,
    "tomas": [
        {
            "x": 42,
            "y": 0
        },
        {
            "x": 0,
            "y": 250
        },
        {
            "x": 0,
            "y": 80
        },
        {
            "x": 400,
            "y": 250
        }
    ],
    "reglas_adyacencia": [ (escritorio, biblioteca), (tv, sillon), (tv, mesa_con_sillas), (lampara, sillon) ],
    "reglas_enfrentamiento": [ (tv, sillon) ]
}

habitacion_2 = {
    "muebles": [ mesa_con_sillas, tv, biblioteca, sillon, escritorio, lampara, heladera, cocina, cama,lavarropas ],
    "ancho": 800,
    "profundidad": 500,
    "tomas": [
        {
            "x": 42,
            "y": 0
        },
        {
            "x": 0,
            "y": 250
        },
        {
            "x": 0,
            "y": 80
        },
        {
            "x": 800,
            "y": 250
        }
    ],
    "reglas_adyacencia": [ (escritorio, biblioteca), (tv, sillon), (tv, mesa_con_sillas), (lampara, sillon), (heladera, cocina), (cama, tv), (lavarropas, heladera) ],
    "reglas_enfrentamiento": [ (tv, sillon) ]
}

HABITACION = habitacion_1
MUEBLES = HABITACION["muebles"]
CANTIDAD_DE_MUEBLES = len(MUEBLES)