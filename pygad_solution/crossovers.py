import numpy as np
import random

def discrete_crossover(parents, offspring_size, ga_instance):
    # TBD
    offspring = np.empty(offspring_size)
    probability = 0.8

    
    for k in range(offspring_size[0]):
        parent1_idx = random.randint(0, parents.shape[0] - 1)
        parent2_idx = random.randint(0, parents.shape[0] - 1)

        values = []

        for val1, val2 in zip(parents[parent1_idx], parents[parent2_idx]):
            
            values.append()

