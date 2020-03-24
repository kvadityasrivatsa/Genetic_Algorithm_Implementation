import random
import numpy as np
from copy import deepcopy
import client
import pickle
import os
from scraper import checkUsage
import keyboard
from time import sleep
import datetime

KEY = "U19pqkBxr6CVL84rqVPHK0lwXqLa1FjST0RWF5FcUIPAmR5kCq"
initial_list = [-0.00016927573251173823, 0.0010953590656607808, 0.003731869524518327, 0.08922889556431182, 0.03587507175384199, -0.0015634754169704097, -7.439827367266828e-05, 3.7168210026033343e-06, 1.555252501348866e-08, -2.2215895929103804e-09, 2.306783174308054e-11]
initial = np.asarray(initial_list)

def calculate_fitness(error):
    return 1/((error[0]*(8) + error[1])/1e5)

NUM_OF_WEIGHTS = 11
EQUALITY_THRESHOLD = 10
x = datetime.datetime.now()
x = str(x)
x = x.replace('.','')
x = x.replace(" ","_")
SAVE_FILE_NAME = "known_"+x+".pickle"

def rand_length(MAX_LENGTH):
    return random.randint(0,MAX_LENGTH)

def crossover(c1, c2):
    c1_contribution = rand_length(NUM_OF_WEIGHTS)
    child_weight1 = np.concatenate((c1[0:c1_contribution], c2[c1_contribution:NUM_OF_WEIGHTS]))
    child_weight2 = np.concatenate((c2[0:c1_contribution], c1[c1_contribution:NUM_OF_WEIGHTS]))
    return [child_weight1, child_weight2]

def mutation(c1):
    c1 = deepcopy(c1)
    index1 = rand_length(NUM_OF_WEIGHTS - 1)
    index2 = rand_length(NUM_OF_WEIGHTS - 1)
    temp = c1[index1]
    c1[index1] = c1[index2]
    c1[index2] = temp
    return c1

def almostEqual(w1, w2):
    return np.sum(abs(w1 - w2) <= w1/EQUALITY_THRESHOLD) > 0

def load_population():
    loaded_population = [new_chromosome(initial), new_chromosome(np.asarray([0.0 for i in range(11)]))]
    if(os.path.exists(SAVE_FILE_NAME)):
        with open(SAVE_FILE_NAME, "rb") as f:
            loaded_population = pickle.load(f)
            f.close()
    return loaded_population

def save_population(population):
    with open(SAVE_FILE_NAME, "wb") as f:
        pickle.dump(population, f)
        f.close()

def find_error(weights, population):
    stop_flag = False
    for chromosome in population:
        if(almostEqual(weights, chromosome[0]) and chromosome[1] != -1):
            return chromosome[2], stop_flag
    # if checkUsage() == 0:
        # stop_flag = True
    # error = client.get_errors(KEY, list(weights))
    error = [random.uniform(10**6, 10**12), random.uniform(10**6, 10**12)]
    return error, stop_flag

def selection(population):
    stop_flag = False
    for chromosome in population:
        weights = chromosome[0]
        fitness = chromosome[1]
        error = chromosome[2]
        if(fitness == -1):
            error, stop_flag = find_error(weights, population)
            if not stop_flag:
                fitness = calculate_fitness(error)
                chromosome[1] = fitness
                chromosome[2] = error
            else:
                return population[:2], stop_flag

    population.sort(key = lambda x: x[1])
    return population[:2], stop_flag

def new_chromosome(weights):
    return [weights, -1, [0, 0]]

def print_population(MAX_COUNT, population):
    MAX_COUNT = min(MAX_COUNT, len(population))
    for i, chromosome in enumerate(population[0:MAX_COUNT]):
        print("##", "Chromosome #", i+1)
        print(chromosome[0])
        print(chromosome[1], chromosome[2])
        print()
    print("=============================================================================")

population = load_population()
while(1):
# for queries in range(70):
    if(keyboard.is_pressed('q')):
        break
    parents, stop_flag = selection(population)
    if(stop_flag):
        break
    children = crossover(parents[0][0], parents[1][0])
    for i in range(2):
        population.append(new_chromosome(mutation(children[i])))
    print_population(4, population)
    sleep(0.01)
    # input()

save_population(population)