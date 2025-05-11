#na podstawie przykładu: https://pypi.org/project/pygad/1.0.18/
import logging
import pygad
import numpy
import benchmark_functions as bf
import numpy as np
from mutations import gauss_mutation
from crossovers import arithmetic_crossover, linear_crossover, alpha_mix_crossover, alpha_beta_mix_crossover, average_crossover

#Konfiguracja algorytmu genetycznego

num_genes = 3
func = bf.Ackley(n_dimensions=num_genes)

num_generations = 100
sol_per_pop = 80
num_parents_mating = 50
init_range_low = -32.768
init_range_high = 32.768
mutation_num_genes = 1
parent_selection_type = "rws"
crossover_type = "two_points"
mutation_type = "random"
num_gens_per_variable = 20

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
    # Decode the binary representation to real values
    decoded_solution = decode(solution, var_n=num_genes, var_range=(init_range_low, init_range_high))
    
    # Evaluate the fitness using the decoded solution
    fitness = func(decoded_solution)
    return 1. / fitness

fitness_function = fitness_func
num_generations = 10
sol_per_pop = 80
num_parents_mating = 50
#boundary = func.suggested_bounds() #możemy wziąć stąd zakresy
init_range_low = -32.768
init_range_high = 32.768
mutation_num_genes = 1
parent_selection_type = "tournament"
crossover_type = "uniform"
mutation_type = "random"


#Konfiguracja logowania

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
    ga_instance.logger.info("Generation = {generation}".format(generation=ga_instance.generations_completed))
    solution, solution_fitness, solution_idx = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)
    ga_instance.logger.info("Best    = {fitness}".format(fitness=1./solution_fitness))
    ga_instance.logger.info("Individual    = {solution}".format(solution=repr(solution)))

    real_function_value = func(decode(solution, var_n=num_genes, var_range=(init_range_low, init_range_high)))
    function_values.append(real_function_value)
    mean_function_values.append(numpy.mean(function_values))
    std_function_values.append(numpy.std(function_values))

    tmp = [1./x for x in ga_instance.last_generation_fitness] #ponownie odwrotność by zrobić sobie dobre statystyki

    ga_instance.logger.info("Min    = {min}".format(min=numpy.min(tmp)))
    ga_instance.logger.info("Max    = {max}".format(max=numpy.max(tmp)))
    ga_instance.logger.info("Average    = {average}".format(average=numpy.average(tmp)))
    ga_instance.logger.info("Std    = {std}".format(std=numpy.std(tmp)))
    ga_instance.logger.info("\r\n")


def plots():

    best = ga_instance.best_solution()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=1./solution_fitness))


    # sztuczka: odwracamy my narysował nam się oczekiwany wykres dla problemu minimalizacji
    ga_instance.best_solutions_fitness = [1. / x for x in ga_instance.best_solutions_fitness]
    ga_instance.plot_fitness()


    plt.plot(function_values, label='Best Ackley Value')
    plt.plot(mean_function_values, label='Mean Ackley Value')
    plt.plot(std_function_values, label='Std Ackley Value')
    plt.xlabel("Generation")
    plt.ylabel("Values")
    plt.title("Function per Generation")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()






ga_instance = pygad.GA(num_generations=num_generations,
          sol_per_pop=sol_per_pop,
          num_parents_mating=num_parents_mating,
          num_genes=num_genes*num_gens_per_variable,
          gene_space=[0, 1],
          fitness_func=fitness_func,
        #   init_range_low=init_range_low,
        #   init_range_high=init_range_high,
          mutation_num_genes=mutation_num_genes,
          parent_selection_type=parent_selection_type,
          crossover_type=linear_crossover,
          mutation_type=gauss_mutation,
          keep_elitism= 1,
          K_tournament=3,
          random_mutation_max_val=32.768,
          random_mutation_min_val=-32.768,
          logger=logger,
          on_generation=on_generation,
          parallel_processing=['thread', 4],
          gene_type=int, 
          init_range_low=0,
          init_range_high=2,
          save_solutions=True)

ga_instance.run()

plots()



