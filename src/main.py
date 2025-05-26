import config
import values
import csv
import random
from deap import base, creator, tools, algorithms

from src.aptitude import fitness
from src.generators import generar_habitacion, generar_set_nuebles


def cx_habitacion(ind1, ind2):
    pass


def mutar_habitacion(ind1, ind2):
    pass

habitacion = generar_habitacion()

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, generar_set_nuebles(habitacion))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", fitness())

if config.CONFIG.SELECTION_TYPE == 'Tournament':
    toolbox.register("select", tools.selTournament, tournsize=config.CONFIG.TOURNAMENT_SIZE)
elif config.CONFIG.SELECTION_TYPE == 'Roulette':
    toolbox.register("select", tools.selRoulette)
elif config.CONFIG.SELECTION_TYPE == 'Rank':
    toolbox.register("select", tools.selRank)

if config.CONFIG.CROSSOVER_TYPE == 'cx_habitacion':
    toolbox.register("mate", cx_habitacion)

toolbox.register("mutate", mutar_habitacion)


def execute_ga_with_deap():
    population = toolbox.population(n=config.CONFIG.POPULATION_SIZE)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda x: sum(fit[0] for fit in x) / len(x))
    stats.register("max", max)

    with open("../resources/resultados.csv", mode="w", newline="") as file:
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
        print(f"Integrante {idx} (ID: {mueble['id']}):")
        for key, value in mueble.items():
            print(f"  {key}: {value}")
    print("Fitness value:", best_habitacion.fitness.values[0])

    with open("../resources/best_habitacion.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["ID", "Nombre", "Ancho", "Profundidad", "x", "y", "Rotacion (0-90°)", "Requiere toma", "Debe ir a pared"])
        for idx, mueble in enumerate(best_habitacion, start=1):
            writer.writerow([f"Mueble {idx}", mueble["id"], mueble["nombre"], mueble["ancho"],
                             mueble["profundidad"], mueble["x"], mueble["y"],
                             mueble["rot"], mueble["requiere_toma"], mueble["debe_ir_a_pared"]])


if __name__ == "__main__":
    execute_ga_with_deap()

"""
def cxBanda(ind1, ind2):
    combined = ind1 + ind2
    random.shuffle(combined)
    tipos_musicos = {}

    for musico in combined:
        tipo = musico["tipo"]
        if tipo not in tipos_musicos:
            tipos_musicos[tipo] = musico

    new_musicos = list(tipos_musicos.values())

    while len(new_musicos) < 5:
        tipo_faltante = random.choice([t for t in values.TIPOS if t not in tipos_musicos])
        nuevo_musico = generar_musico()
        nuevo_musico["tipo"] = tipo_faltante
        new_musicos.append(nuevo_musico)

    ind1[:] = new_musicos[:5]
    ind2[:] = new_musicos[:5]

    return ind1, ind2

def mutar_banda(individual):
    for i in range(len(individual)):
        if random.random() < config.CONFIG.MUTATION_PROB:
            tipo = individual[i]["tipo"]
            id_original = individual[i]["id"]
            nuevo_musico = generar_musico()

            # Mantener el ID original y el tipo
            nuevo_musico["id"] = id_original
            nuevo_musico["tipo"] = tipo

            individual[i] = nuevo_musico
    return individual,
"""
