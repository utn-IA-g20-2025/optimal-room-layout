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
MUEBLES = [
    {

        "nombre": "Mesa con sillas",
        "ancho": 95,
        "profundidad": 160,
        "necesita_toma": False,
        "lado_frontal": None,
        "margen_a": 20,
        "margen_b": 20,
        "margen_c": 20,
        "margen_d": 20

    },
    {
        "nombre": "Cama",
        "ancho": 140,
        "profundidad": 190,
        "necesita_toma": False,
        "lado_frontal": None,
        "margen_a": 25,
        "margen_b": 25,
        "margen_c": 25,
        "margen_d": 25
    },
    {
        "nombre": "TV",
        "ancho": 8,
        "profundidad": 145,
        "necesita_toma": True,
        "lado_frontal": "B",
        "margen_a": 20,
        "margen_b": 80,
        "margen_c": 20,
        "margen_d": 20
    },
    {
        "nombre": "Biblioteca",
        "ancho": 60,
        "profundidad": 40,
        "necesita_toma": False,
        "lado_frontal": "B",
        "margen_a": 5,
        "margen_b": 40,
        "margen_c": 5,
        "margen_d": 5
    },
    {
        "nombre": "Sillón",
        "ancho": 80,
        "profundidad": 180,
        "necesita_toma": False,
        "lado_frontal": "D",
        "margen_a": 0,
        "margen_b": 0,
        "margen_c": 0,
        "margen_d": 60
    },
    {
        "nombre": "Escritorio",
        "ancho": 60,
        "profundidad": 120,
        "necesita_toma": False,
        "lado_frontal": "B",
        "margen_a": 5,
        "margen_b": 60,
        "margen_c": 5,
        "margen_d": 5
    },
    {
        "nombre": "Lavarropas",
        "ancho": 54,
        "profundidad": 54,
        "necesita_toma": True,
        "lado_frontal": "A",
        "margen_a": 40,
        "margen_b": 10,
        "margen_c": 10,
        "margen_d": 10
    },
    {
        "nombre": "Heladera",
        "ancho": 60,
        "profundidad": 64,
        "necesita_toma": True,
        "lado_frontal": "B",
        "margen_a": 10,
        "margen_b": 60,
        "margen_c": 10,
        "margen_d": 15
    }
]

HABITACION = {
    "ancho": 400,
    "profundidad": 500,
    "tomas": [
        {
            "x": 42,
            "y": 0
        },
        {
            "x": 0,
            "y": 60
        },
        {
            "x": 0,
            "y": 80
        }
    ],
    "reglas_adyacencia": [] # TODO reglas_adyacencia: lista de tuplas con nombres de objetos que deben estar juntos.
}


TIPOS = ["Mesa con sillas", "Cama","TV","Biblioteca","sillón", "Escritorio", "Lavarropas"]

CANTIDAD_DE_MUEBLES = len(TIPOS)