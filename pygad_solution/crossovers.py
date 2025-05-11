import numpy as np
import random

def arithmetic_crossover(parents, offspring_size, ga_instance):

    offspring = np.empty(offspring_size)

    for k in range(offspring_size[0]):
        parent1_idx = random.randint(0, parents.shape[0] - 1)
        parent2_idx = random.randint(0, parents.shape[0] - 1)
        alpha = np.random.rand()
        values = []
        for val1, val2 in zip(parents[parent1_idx], parents[parent2_idx]):
            values.append(alpha * val1 + (1 - alpha) * val2)

        offspring[k] = values

    return offspring

def linear_crossover(parents, offspring_size, ga_instance):
    const1 = 1/2
    const2 = 3/2
    offspring = np.empty(offspring_size)

    for k in range(offspring_size[0]):
        parent1_idx = random.randint(0, parents.shape[0] - 1)
        parent2_idx = random.randint(0, parents.shape[0] - 1)
        child1_val = []
        child2_val = []
        child3_val = []
        find = False
        while not find:
            for val1, val2 in zip(parents[parent1_idx], parents[parent2_idx]):
                child1_val.append(const1 * val1 + const1* val2)
                child2_val.append(const2 * val1 - const1* val2)
                child3_val.append(-const1 * val1 + const2* val2)
            

            values = [child1_val, child2_val, child3_val]
            values.sort()
            for val in values:
                counter = 0
                for i in val:
                    if i >= ga_instance.init_range_low and i <= ga_instance.init_range_high:
                        counter += 1
                if counter == len(val):
                    find = True
                    offspring[k] = val
                    break

    return offspring


def alpha_mix_crossover(parents, offspring_size, ga_instance):

    offspring = np.empty(offspring_size)
    alpha = 0.5

    for k in range(offspring_size[0]):
        parent1_idx = random.randint(0, parents.shape[0] - 1)
        parent2_idx = random.randint(0, parents.shape[0] - 1)
        alpha = np.random.rand()
        final_values = []
        for val1, val2 in zip(parents[parent1_idx], parents[parent2_idx]):
            d = abs(val1 - val2)
            values = [min(val1, val2) - alpha*d, max(val1, val2) + alpha*d]
            curr_val = random.uniform(values[0], values[1])
            while curr_val < ga_instance.init_range_low or curr_val > ga_instance.init_range_high:
                curr_val = random.uniform(values[0], values[1])
            final_values.append(curr_val)

        offspring[k] = final_values

    return offspring

def alpha_beta_mix_crossover(parents, offspring_size, ga_instance):
 
    offspring = np.empty(offspring_size)
    alpha = 0.5
    beta = 0.5

    for k in range(offspring_size[0]):
        parent1_idx = random.randint(0, parents.shape[0] - 1)
        parent2_idx = random.randint(0, parents.shape[0] - 1)
        alpha = np.random.rand()
        final_values = []
        for val1, val2 in zip(parents[parent1_idx], parents[parent2_idx]):
            d = abs(val1 - val2)
            values = [min(val1, val2) - alpha*d, max(val1, val2) + beta*d]
            curr_val = random.uniform(values[0], values[1])
            while curr_val < ga_instance.init_range_low or curr_val > ga_instance.init_range_high:
                curr_val = random.uniform(values[0], values[1])
            final_values.append(curr_val)

        offspring[k] = final_values

    return offspring


def average_crossover(parents, offspring_size, ga_instance):

    offspring = np.empty(offspring_size)

    for k in range(offspring_size[0]):
        parent1_idx = random.randint(0, parents.shape[0] - 1)
        parent2_idx = random.randint(0, parents.shape[0] - 1)
        values = []
        for val1, val2 in zip(parents[parent1_idx], parents[parent2_idx]):
            values.append((val1 + val2) / 2)

        offspring[k] = values

    return offspring