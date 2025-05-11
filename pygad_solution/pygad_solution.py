#na podstawie przykładu: https://pypi.org/project/pygad/1.0.18/
import logging
import pygad
import numpy
import benchmark_functions as bf
from mutations import gauss_mutation
from crossovers import arithmetic_crossover, linear_crossover, alpha_mix_crossover, alpha_beta_mix_crossover, average_crossover
import matplotlib.pyplot as plt
import time
from opfunu.cec_based import F12010
from copy import deepcopy


num_genes = 10

# func = bf.Hypersphere(num_genes)
func = F12010(ndim=num_genes).evaluate

binary_representation = False

function_values = []
mean_function_values = []
std_function_values = []


def decode(individual, var_n, var_range):
    '''
    Funkcja do dekodowania osobnika z postaci binarnej na dziesiętną, ciag binarny wszystkich genów

    '''
    a, b = var_range
    decoded = []
    gen_length = len(individual) // var_n
    for i in range(var_n):
        start = i * gen_length
        end = (i + 1) * gen_length
        binary_chain = individual[start:end]
        decimal_repr = int("".join(map(str, binary_chain)), 2)
        val = a + decimal_repr * (b - a) / (2**gen_length - 1)
        decoded.append(val)

    return decoded

def fitness_func(ga_instance, solution, solution_idx):
    if binary_representation:
        decoded_solution = decode(solution, var_n=num_genes, var_range=(init_range_low, init_range_high))
        fitness = func(decoded_solution)
    else:
        fitness = func(solution)
    return 1. / fitness


fitness_function = fitness_func
num_gens_per_variable = 20
num_generations = 100
sol_per_pop = 80
num_parents_mating = 50
boundary = func.suggested_bounds()
init_range_low = boundary[0][0]
init_range_high = boundary[1][0]

# for Opfun function
# init_range_low = -10
# init_range_high = 10

mutation_num_genes = 1
parent_selection_type = "tournament"

if binary_representation:
    crossover_type = "uniform"
    mutation_type = "swap"
else:
    crossover_type = linear_crossover
    mutation_type = gauss_mutation

level = logging.DEBUG
name = 'logfile.txt'
logger = logging.getLogger(name)
logger.setLevel(level)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = logging.Formatter('%(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)


def on_generation(ga_instance):
    solution, solution_fitness, solution_idx = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)
    if ga_instance.generations_completed % 100 == 0:

        ga_instance.logger.info("Generation = {generation}".format(generation=ga_instance.generations_completed))
        ga_instance.logger.info("Best    = {fitness}".format(fitness=1./solution_fitness))
        ga_instance.logger.info("Individual    = {solution}".format(solution=repr(solution)))

    real_function_value = func(decode(solution, var_n=num_genes, var_range=(init_range_low, init_range_high))) if binary_representation else func(solution)
    function_values.append(real_function_value)
    mean_function_values.append(numpy.mean(function_values))
    std_function_values.append(numpy.std(function_values))

    tmp = [1./x for x in ga_instance.last_generation_fitness] #ponownie odwrotność by zrobić sobie dobre statystyki

    if ga_instance.generations_completed % 100 == 0:
        ga_instance.logger.info("Min    = {min}".format(min=numpy.min(tmp)))
        ga_instance.logger.info("Max    = {max}".format(max=numpy.max(tmp)))
        ga_instance.logger.info("Average    = {average}".format(average=numpy.average(tmp)))
        ga_instance.logger.info("Std    = {std}".format(std=numpy.std(tmp)))
        ga_instance.logger.info("\r\n")


def plots():

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=1./solution_fitness))

    # sztuczka: odwracamy my narysował nam się oczekiwany wykres dla problemu minimalizacji
    ga_instance.best_solutions_fitness = [1. / x for x in ga_instance.best_solutions_fitness]
    ga_instance.plot_fitness()

    plt.plot(function_values, label='Best Value')
    plt.plot(mean_function_values, label='Mean Value')
    plt.plot(std_function_values, label='Std Value')
    plt.xlabel("Generation")
    plt.ylabel("Values")
    plt.title(f"{crossover_type} - {mutation_type} - {parent_selection_type} - {num_genes}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def binary_simulation():
    ga_instance = pygad.GA(num_generations=num_generations,
            sol_per_pop=sol_per_pop,
            num_parents_mating=num_parents_mating,
            num_genes=num_genes*num_gens_per_variable,
            gene_space=[0, 1],
            fitness_func=fitness_func,
            mutation_percent_genes = 10,
            mutation_num_genes=mutation_num_genes,
            parent_selection_type=parent_selection_type,
            crossover_type=crossover_type,
            mutation_type=mutation_type,
            keep_elitism= 1,
            K_tournament=3,
            random_mutation_max_val=init_range_high,
            random_mutation_min_val=init_range_low,
            logger=logger,
            on_generation=on_generation,
            parallel_processing=['thread', 4],
            gene_type=int, 
            init_range_high=2,
            init_range_low=0,)
    
    return ga_instance

def real_simulation():
    ga_instance = pygad.GA(num_generations=num_generations,
            sol_per_pop=sol_per_pop,
            num_parents_mating=num_parents_mating,
            num_genes=num_genes,
            fitness_func=fitness_func,
            mutation_percent_genes = 10,
            mutation_num_genes=mutation_num_genes,
            parent_selection_type=parent_selection_type,
            crossover_type=crossover_type,
            mutation_type=mutation_type,
            keep_elitism= 1,
            K_tournament=3,
            random_mutation_max_val=init_range_high,
            random_mutation_min_val=init_range_low,
            logger=logger,
            on_generation=on_generation,
            parallel_processing=['thread', 4],
            gene_type=float)
    
    return ga_instance

all_solutions = []
all_times = []

all_function_values = []
all_mean_function_values = []
all_std_function_values = []
for i in range(10):
    ga_instance = real_simulation() if not binary_representation else binary_simulation()
    function_values.clear()
    mean_function_values.clear()
    std_function_values.clear()

    start_time = time.time()
    ga_instance.run()
    end_time = time.time()
    print("Time: ", end_time - start_time)
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    all_solutions.append(1./solution_fitness)
    all_times.append(end_time - start_time)

    all_function_values.append(function_values)
    all_mean_function_values.append(mean_function_values)
    all_std_function_values.append(std_function_values)


after_sort = deepcopy(all_solutions)
all_solutions.sort()
print("Best solution: ", all_solutions[0])

best_solution_idx = after_sort.index(all_solutions[0])

values = all_function_values[best_solution_idx]
mean_values = all_mean_function_values[best_solution_idx]
std_values = all_std_function_values[best_solution_idx]

print("Average time: ", sum(all_times) / len(all_times))
print("Average solution: ", sum(all_solutions) / len(all_solutions))
plots()



