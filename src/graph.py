import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.aptitude import sentido_por_lado_segun_rotacion


def dibujar_margen(ax, x0, y0, margen, angulo, ancho_mueble, profundidad_mueble):
    if angulo == 90:
        ax.add_patch(patches.Rectangle((x0, y0 + profundidad_mueble),
                                       ancho_mueble, margen,
                                       linewidth=1, edgecolor='gray',
                                       linestyle='dotted', fill=False))
    elif angulo == 0:
        ax.add_patch(patches.Rectangle((x0 + ancho_mueble, y0),
                                       margen, profundidad_mueble,
                                       linewidth=1, edgecolor='gray',
                                       linestyle='dotted', fill=False))
    elif angulo == 270:
        ax.add_patch(patches.Rectangle((x0, y0 - margen),
                                       ancho_mueble, margen,
                                       linewidth=1, edgecolor='gray',
                                       linestyle='dotted', fill=False))
    if angulo == 180:
        ax.add_patch(patches.Rectangle((x0 - margen, y0),
                                       margen, profundidad_mueble,
                                       linewidth=1, edgecolor='gray',
                                       linestyle='dotted', fill=False))

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

        lado_frontal = m["lado_frontal"]
        if lado_frontal:
            sentido = sentido_por_lado_segun_rotacion[rot][lado_frontal]

            if sentido == 90: # arriba
                fx, fy = x, y + profundidad / 2
                dx, dy = 0, 10
            elif sentido == 0: # derecha
                fx, fy = x + ancho / 2, y
                dx, dy = 10, 0
            elif sentido == 270: # abajo
                fx, fy = x, y - profundidad / 2
                dx, dy = 0, -10
            else: # 180, izquierda
                fx, fy = x - ancho / 2, y
                dx, dy = -10, 0

            # Coordenadas de inicio de la flecha (centro del lado frontal)
            ax.arrow(fx, fy, dx, dy, head_width=5, head_length=5, fc='green', ec='green')


        # Dibujar márgenes
        margen_a, margen_b, margen_c, margen_d = m["margen_a"], m["margen_b"], m["margen_c"], m["margen_d"]

        if margen_a and margen_a > 0:
            dibujar_margen(ax, x0, y0, margen_a, sentido_por_lado_segun_rotacion[rot]["a"], ancho, profundidad)
        if margen_b and margen_b > 0:
            dibujar_margen(ax, x0, y0, margen_b, sentido_por_lado_segun_rotacion[rot]["b"], ancho, profundidad)
        if margen_c and margen_c > 0:
            dibujar_margen(ax, x0, y0, margen_c, sentido_por_lado_segun_rotacion[rot]["c"], ancho, profundidad)
        if margen_d and margen_d > 0:
            dibujar_margen(ax, x0, y0, margen_d, sentido_por_lado_segun_rotacion[rot]["d"], ancho, profundidad)


    plt.grid(True)
    plt.show()
