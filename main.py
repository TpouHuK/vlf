import random
import numpy as np
np.random.seed(2020)
random.seed(2020)

from deap import base
from deap import creator
from deap import tools

import vlf
import checkpoints

POPULATION_SIZE = 10
NEW_EVERY_DAY = 2
DIES_EVERY_DAY = int(POPULATION_SIZE*0.4)
ALIVE_EVERY_DAY = POPULATION_SIZE - DIES_EVERY_DAY
DIE_TOURN_SIZE = 3
BREED_TOURN_SIZE = 3
MUTATED_EVERY_DAY = 2

brain = vlf.neural_network.FFNeuralNetwork()

c = vlf.get_fitness.Course(checkpoints.ch_list)

def breed_brains(a, b):
    f_a = a.get_flattened_array()
    f_b = b.get_flattened_array()
    new_gen = np.array([random.choice((x, y)) for x, y in zip(f_a, f_b)])

    new_boi = vlf.neural_network.FFNeuralNetwork()
    new_boi.assemble_from_flattened(new_gen)
    return new_boi

def mutate_brain(a, chance=3/23):
    flat_arr = a.get_flattened_array()
    for i in range(len(flat_arr)):
        if random.random() < chance:
            flat_arr[i] *= random.random()*2
    a.assemble_from_flattened(flat_arr)
    #return FFNeuralNetwork().assemble_from_flattened(flat_arr)

def get_fitness(brain):
    return c.check_fitness(brain.get_result)

population = [vlf.neural_network.FFNeuralNetwork() for i in range(POPULATION_SIZE)]
fitnesses = [get_fitness(p) for p in population]

for p, f in zip(population, fitnesses):
    p.fitness = f

g = 0
while True:
    g += 1
    survivors = tools.selTournament(population, ALIVE_EVERY_DAY, DIE_TOURN_SIZE, fit_attr="fitness")

    childs = []
    for i in range(DIES_EVERY_DAY - NEW_EVERY_DAY):
        a, b = tools.selTournament(survivors, 2, BREED_TOURN_SIZE, fit_attr="fitness")
        child = breed_brains(a, b)
        child.fitness = None
        childs.append(child)

    for i in range(NEW_EVERY_DAY):
        new = vlf.neural_network.FFNeuralNetwork()
        new.fitness = None
        survivors.append(new)

    mutants = tools.selRandom(survivors, MUTATED_EVERY_DAY)
    for m in mutants:
        mutate_brain(m)
        m.fitness = None

    population = survivors + childs

    for p in population:
        if not p.fitness:
            p.fitness = get_fitness(p)

    f = [p.fitness for p in population]
    print("GENERATION", g)
    print("MEAN:", sum(f)/len(f))
    print("MAX:", max(f))
    print("MIN:", min(f))
    print("=+======+=")
