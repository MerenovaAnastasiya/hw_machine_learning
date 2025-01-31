"""
The equation: 1027 * x + 712 * y = 1
D(x) = [-1 500; 1 500]
D(y) = [-1 500; 1 500]
"""
import random
import operator

from deap import tools, base, creator, algorithms


MUT_MIN, MUT_MAX = -10, 10
NGEN, IND_SIZE, CXPB, MUTPB, TRN_SIZE = 100, 50, 0.5, 0.5, 100
HALL_SIZE = 10
DEFAULT_MAIN_ARGS = NGEN, IND_SIZE, CXPB, MUTPB

MIN, MAX = -3000, 3000
SOLUTION = [-165, 165]
VARIABLES = len(SOLUTION)

BEST_INSTANCE_MSG = 'Лучший экземпляр поколения:'
NO_SOLUTION_MSG = 'Нет решения для целых числе. Дистанция:'


def fitness_function(instance):
    x, y = instance
    return abs(1029 * x + 541 * y - 1),


def mutate(instance, mutpb):
    if random.random() <= mutpb:
        index = random.randint(0, len(instance) - 1)
        instance[index] += random.randint(MUT_MIN, MUT_MAX)
        return instance,
    return instance,


def get_best_result(population):
    if isinstance(population[0], list):
        fitness_values = list(map(fitness_function, population))
        index = fitness_values.index(min(fitness_values))
        return population[index]
    else:
        return min(population, key=operator.attrgetter('fitness'))


def terminate(population):
    if fitness_function(get_best_result(population)) == (0,):
        raise StopIteration
    return False


def distance_from_best_result(population):
    result = get_best_result(population)
    return fitness_function(result)[0]


def output(best_instance):
    print(BEST_INSTANCE_MSG, best_instance)
    distance = fitness_function(best_instance)
    if distance:
        print(NO_SOLUTION_MSG, distance)


def setup(mutpb):
    creator.create("FitnessMin", base.Fitness, weights=(-1,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("attribute", random.randint, MIN, MAX)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attribute, n=VARIABLES)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", mutate, mutpb=mutpb)
    toolbox.register("select", tools.selBest)
    toolbox.register("evaluate", fitness_function)
    return toolbox


def main(ngen, ind_size, cxpb, mutpb):
    toolbox = setup(ind_size)
    population = toolbox.population(n=ind_size)
    stats = tools.Statistics()
    stats.register("best_instance_of_population", get_best_result)
    stats.register("distance", distance_from_best_result)
    stats.register("terminate", terminate)
    halloffame = tools.HallOfFame(HALL_SIZE)
    try:
        algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen,
                            stats=stats, halloffame=halloffame)
    except StopIteration:
        pass
    finally:
        best_instance = halloffame[0]
        output(best_instance)
        return best_instance


if __name__ == '__main__':
    main(*DEFAULT_MAIN_ARGS)