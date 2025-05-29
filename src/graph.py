import matplotlib.pyplot as plt
import matplotlib.patches as patches

def dibujar_habitacion(muebles, habitacion):
    fig, ax = plt.subplots()
    ax.set_xlim(0, habitacion["ancho"])
    ax.set_ylim(0, habitacion["profundidad"])
    ax.set_aspect('equal')
    ax.set_title("Distribución de Muebles")

    # Dibujar el contorno de la habitación
    ax.add_patch(patches.Rectangle((0, 0), habitacion["ancho"], habitacion["profundidad"],
                                   edgecolor='black', fill=False, linewidth=2))

    # Dibujar los tomacorrientes
    for toma in habitacion["tomas"]:
        ax.plot(toma["x"], toma["y"], marker='o', color='red')
        ax.text(toma["x"] + 3, toma["y"] + 3, 'Toma', color='red', fontsize=8)

    # Lados para márgenes
    lados = ['a', 'b', 'c', 'd']

    # Dibujar cada mueble
    for m in muebles:
        x, y = m["x"], m["y"]
        ancho = m["ancho"]
        profundidad = m["profundidad"]
        rot = m["rot"]

        # Ajuste por rotación
        if rot in [90, 270]:
            ancho, profundidad = profundidad, ancho

        x0 = x - ancho / 2
        y0 = y - profundidad / 2

        # Dibujar el mueble
        mueble = patches.Rectangle((x0, y0), ancho, profundidad,
                                   linewidth=1, edgecolor='blue', facecolor='lightblue')
        ax.add_patch(mueble)
        ax.text(x, y, m["nombre"],
                ha='center', va='center', fontsize=8)

        # Dibujar márgenes como líneas punteadas
        margenes = {
            'a': m['margen_a'],
            'b': m['margen_b'],
            'c': m['margen_c'],
            'd': m['margen_d']
        }

        lado_frontal = m["lado_frontal"]
        if lado_frontal:
            lado_to_angulo = {'a': 90, 'b': 0, 'c': 270, 'd': 180}
            angulo_frontal = (lado_to_angulo[lado_frontal] + m["rot"]) % 360

            # Coordenadas de inicio de la flecha (centro del lado frontal)
            if angulo_frontal == 0:  # Derecha
                fx, fy = x, y
                dx, dy = 10, 0
            elif angulo_frontal == 90:  # Arriba
                fx, fy = x, y
                dx, dy = 0, 10
            elif angulo_frontal == 180:  # Izquierda
                fx, fy = x, y
                dx, dy = -10, 0
            elif angulo_frontal == 270:  # Abajo
                fx, fy = x, y
                dx, dy = 0, -10

            ax.arrow(fx, fy, dx, dy, head_width=5, head_length=5, fc='green', ec='green')


        # Ajustar según rotación
        rot_map = {0: ['b', 'a', 'd', 'c'],
                   90: ['a', 'd', 'c', 'b'],
                   180: ['d', 'c', 'b', 'a'],
                   270: ['c', 'b', 'a', 'd']}
        rotados = rot_map[rot]
        margenes_rotados = {lado: margenes[rotados[i]] for i, lado in enumerate(lados)}

        # Dibujar cada margen
        if margenes_rotados['a'] > 0:
            ax.add_patch(patches.Rectangle((x0, y0 + profundidad),
                                           ancho, margenes_rotados['a'],
                                           linewidth=1, edgecolor='gray',
                                           linestyle='dotted', fill=False))
        if margenes_rotados['b'] > 0:
            ax.add_patch(patches.Rectangle((x0 - margenes_rotados['b'], y0),
                                           margenes_rotados['b'], profundidad,
                                           linewidth=1, edgecolor='gray',
                                           linestyle='dotted', fill=False))
        if margenes_rotados['c'] > 0:
            ax.add_patch(patches.Rectangle((x0, y0 - margenes_rotados['c']),
                                           ancho, margenes_rotados['c'],
                                           linewidth=1, edgecolor='gray',
                                           linestyle='dotted', fill=False))
        if margenes_rotados['d'] > 0:
            ax.add_patch(patches.Rectangle((x0 + ancho, y0),
                                           margenes_rotados['d'], profundidad,
                                           linewidth=1, edgecolor='gray',
                                           linestyle='dotted', fill=False))

    #plt.gca().invert_yaxis()  # Para que (0,0) esté en la esquina superior izquierda
    plt.grid(True)
    plt.show()
