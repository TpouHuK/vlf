import random
import numpy as np
np.random.seed(2020)
random.seed(2020)

from deap import base
from deap import creator
from deap import tools
from PIL import Image

import vlf
import checkpoints

# Total amout of line followers
POPULATION_SIZE = 100

# Amount of random line followers every day
NEW_EVERY_DAY = 4

# Amout of removed line followers
DIES_EVERY_DAY = int(POPULATION_SIZE*0.3)

ALIVE_EVERY_DAY = POPULATION_SIZE - DIES_EVERY_DAY

# Smaller number -> more weak line followers survive
# Bigger number -> more strong line followers survive
# Cant be bigger that POPULATION_SIZE
DIE_TOURN_SIZE = int(POPULATION_SIZE*0.3)

# Smaller number -> more weak line followers have chance to breed
# Bigger number -> more strong line followers have chance to breed
# Cant be bigger that ALIVE_EVERY_DAY
BREED_TOURN_SIZE = int(ALIVE_EVERY_DAY*0.3)

# Amount of mutated line followers every day
# Cant be bigger that ALIVE_EVERY_DAY
MUTATED_EVERY_DAY = 30


assert DIE_TOURN_SIZE <= POPULATION_SIZE
assert BREED_TOURN_SIZE <= ALIVE_EVERY_DAY
assert MUTATED_EVERY_DAY <= ALIVE_EVERY_DAY
assert NEW_EVERY_DAY < DIES_EVERY_DAY

brain = vlf.neural_network.FFNeuralNetwork()

c = vlf.get_fitness.Course(checkpoints.ch_list)

field_image = Image.open("field.png")
field_image = field_image.resize((300, 160))
vis = vlf.visualise.Visualisator()
vis.set_image(field_image)

def breed_brains(a, b):
    f_a = a.get_flattened_array()
    f_b = b.get_flattened_array()
    new_gen = np.array([random.choice((x, y)) for x, y in zip(f_a, f_b)])

    new_boi = vlf.neural_network.FFNeuralNetwork()
    new_boi.assemble_from_flattened(new_gen)
    return new_boi

def mutate_brain(a, chance=1/23):
    flat_arr = a.get_flattened_array()
    for i in range(len(flat_arr)):
        if random.random() < chance:
            flat_arr[i] *= random.random()*2
    a.assemble_from_flattened(flat_arr)
    #return FFNeuralNetwork().assemble_from_flattened(flat_arr)

def get_fitness(brain):
    def ride_func(sensors):
        s = [i/80 for i in sensors]
        x, y = brain.get_result(s)
        return (x)*100, (y)*100

    return c.check_fitness(ride_func)
    #return c.check_fitness(ride_func, visualiser=vis)

def show(brain):
    return
    def ride_func(sensors):
        s = [i/80 for i in sensors]
        x, y = brain.get_result(s)
        return (x-0.5)*100*2, (y-0.5)*100*2*2

    return c.check_fitness(ride_func, visualiser=vis)

population = [vlf.neural_network.FFNeuralNetwork() for i in range(POPULATION_SIZE)]
#a = population[0].get_result((0, 0, 1000, 0))
#print(a)
#print(population[0].get_flattened_array())
#show(population[3])
#exit()
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
    best = max(population, key=lambda x: x.fitness)
    show(best)
    print("GENERATION", g)
    print("MEAN:", sum(f)/len(f))
    print("MAX:", max(f))
    print("MIN:", min(f))
    print("=+======+=")
