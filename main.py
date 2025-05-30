import csv
import random

from deap import base, creator, tools

from src import config
from src.aptitude import fitness, calcular_bounding_box, se_solapan
from src.generators import generar_mueble, generar_set_muebles
from src.values import CANTIDAD_DE_MUEBLES, MUEBLES, HABITACION
from src.graph import dibujar_habitacion
from itertools import combinations

"""
    Genera hijos eligiendo el mueble de uno u otro padre de forma aleatoria
    Args:
        padre1: Lista de muebles de un padre 
        padre2: Lista de muebles de otro padre
    Returns:
        hijo1, hijo2: Par de hijos, cada uno es una lista de muebles
    Ejemplo:
        padre1: [{ "nombre":"Heladera", "x":20, ... }, { "nombre":"Escritorio", "x":100, ... }, ...]
        padre2: [{ "nombre":"Heladera", "x":250, ... }, { "nombre":"Escritorio", "x":80, ... }, ...]
        hijo1: [{ "nombre":"Heladera", "x":250, ... }, { "nombre":"Escritorio", "x":100, ... }, ...]
        hijo2: [{ "nombre":"Heladera", "x":20, ... }, { "nombre":"Escritorio", "x":80, ... }, ...]
"""
def crossover_binomial_azar(padre1, padre2):
    hijo1 = [random.choice([mueble_padre1, mueble_padre2]) for (mueble_padre1, mueble_padre2) in zip(padre1, padre2)]
    hijo2 = [random.choice([mueble_padre1, mueble_padre2]) for (mueble_padre1, mueble_padre2) in zip(padre1, padre2)]
    return hijo1, hijo2

def cx_habitacion(ind1, ind2):
    combined = ind1 + ind2
    random.shuffle(combined)
    muebles = {}

    for mueble in combined:
        nombre = mueble["nombre"]
        if nombre not in muebles:
            muebles[nombre] = mueble

    new_muebles = list(muebles.values())

    while len(new_muebles) < CANTIDAD_DE_MUEBLES:
        mueble_faltante = random.choice([mueble for mueble in MUEBLES if mueble["nombre"] not in muebles])
        nuevo_mueble = generar_mueble(mueble_faltante)
        new_muebles.append(nuevo_mueble)

    ind1[:] = new_muebles[:CANTIDAD_DE_MUEBLES]
    ind2[:] = new_muebles[:CANTIDAD_DE_MUEBLES]

    return ind1, ind2


def mutar_habitacion(individual):
    for i in range(len(individual)):
        if random.random() < config.CONFIG.MUTATION_PROB:
            nuevo_mueble = generar_mueble(individual[i])
            individual[i] = nuevo_mueble

    return individual


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, generar_set_muebles)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", fitness)

if config.CONFIG.SELECTION_TYPE == 'Tournament':
    toolbox.register("select", tools.selTournament, tournsize=config.CONFIG.TOURNAMENT_SIZE)
elif config.CONFIG.SELECTION_TYPE == 'Roulette':
    toolbox.register("select", tools.selRoulette)
elif config.CONFIG.SELECTION_TYPE == 'Rank':
    toolbox.register("select", tools.selRank)

if config.CONFIG.CROSSOVER_TYPE == 'cx_habitacion':
    toolbox.register("mate", crossover_binomial_azar)

toolbox.register("mutate", mutar_habitacion)


def execute_ga_with_deap():
    print("ancho habitacion: ", HABITACION["ancho"])
    print("profundidad habitacion: ", HABITACION["profundidad"])

    population = toolbox.population(n=config.CONFIG.POPULATION_SIZE)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda x: sum(fit[0] for fit in x) / len(x))
    stats.register("max", max)

    with open("resources/resultados.csv", mode="w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Generación", "Fitness Promedio", "Fitness Máximo"])

        for gen in range(config.CONFIG.NUMBER_OF_GENERATIONS):
            offspring = toolbox.select(population, len(population))
            offspring = list(map(toolbox.clone, offspring))

            if gen % config.CONFIG.GENERATIONAL_LEAP == 0:
                for child1, child2 in zip(offspring[::2], offspring[1::2]):
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                toolbox.mutate(mutant)
                del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            population[:] = offspring
            record = stats.compile(population)
            hof.update(population)

            writer.writerow([gen, record["avg"], record["max"]])

            print(f"Generación {gen}: {record}")

    best_habitacion = hof[0]
    print("Best individual:")
    for idx, mueble in enumerate(best_habitacion, start=1):
        print(f"Integrante {idx} (nombre: {mueble['nombre']}):")
        for key, value in mueble.items():
            print(f"  {key}: {value}")
    print("Fitness value:", best_habitacion.fitness.values[0])
    # TODO eliminar, es para debug
    print("Se solapan: ", [(m1["nombre"],m2["nombre"]) for (m1, m2) in combinations(best_habitacion, 2) if se_solapan(calcular_bounding_box(m1),calcular_bounding_box(m2))])

    with open("resources/best_habitacion.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Mueble", "Ancho", "Profundidad", "x", "y", "Rotacion", "Bounding Box", "Requiere toma"])
        for mueble in best_habitacion:
            writer.writerow([mueble["nombre"], mueble["ancho"],
                             mueble["profundidad"], mueble["x"], mueble["y"],
                             mueble["rot"], calcular_bounding_box(mueble), mueble["requiere_toma"]])

    dibujar_habitacion(best_habitacion, HABITACION)


if __name__ == "__main__":
    execute_ga_with_deap()
