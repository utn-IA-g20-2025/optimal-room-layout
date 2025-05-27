"""
                                     90°
 y ^     w                           ^                       A
   |   +--+                          |                     +--+            A=C
   |   |  |  l              180° <-     -> 0°            D |  | B          B=D
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
class Object:
    def __init__(self, name, width, length, powered, front_side, margin_a, margin_b, margin_c, margin_d):
        self.name = name
        self.width = width
        self.length = length
        self.power = powered
        self.front_side = front_side
        self.margin_a = margin_a
        self.margin_b = margin_b
        self.margin_c = margin_c
        self.margin_d = margin_d

OBJECTS = [
    Object(name="Mesa con sillas", width=95, length=160, powered=False, front_side=None, margin_a=20, margin_b=20, margin_c=20, margin_d=20),
    Object(name="Cama", width=140, length=190, powered=False, front_side=None, margin_a=25, margin_b=25, margin_c=25, margin_d=25),
    Object(name="TV", width=8, length=145, powered=True, front_side="B", margin_a=20, margin_b=80, margin_c=20, margin_d=20),
    Object(name="Biblioteca", width=60, length=40, powered=False, front_side="B", margin_a=5, margin_b=40, margin_c=5, margin_d=5),
    Object(name="Sillón", width=80, length=180, powered=False, front_side="D", margin_a=0, margin_b=0, margin_c=0, margin_d=60),
    Object(name="Escritorio", width=60, length=120, powered=False, front_side="B", margin_a=5, margin_b=60, margin_c=5, margin_d=5),
    Object(name="Lavarropas", width=54, length=54, powered=True, front_side="A", margin_a=40, margin_b=10, margin_c=10, margin_d=10),
    Object(name="Heladera", width=60, length=64, powered=True, front_side="B", margin_a=10, margin_b=60, margin_c=10, margin_d=15)
]

TIPOS = ["Mesa con sillas", "Cama","TV","Biblioteca","sillón", "Escritorio", "Lavarropas"]

CANT_MAX_MUEBLES = len(TIPOS)
