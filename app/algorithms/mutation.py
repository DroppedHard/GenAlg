from app.representation.population import Population
from app.representation.individual import Individual
import math
import random
from typing import List
import numpy as np

class Mutation:
    def __init__(self, mutation_rate: float = 0.1):
        if not (0 <= mutation_rate <= 1):
            raise ValueError("mutation_rate must be between 0 and 1")
        self.mutation_rate = mutation_rate

    def should_mutate(self) -> bool:
        return random.random() < self.mutation_rate

    def boundary_mutation(self, individual: 'Individual'):
        if self.should_mutate():
            if random.random() < 0.5:
                individual.genotype[0] ^= 1
            else:
                individual.genotype[-1] ^= 1

    def single_point_mutation(self, individual: 'Individual'):
        if self.should_mutate():
            index = random.randint(0, len(individual.genotype) - 1)
            individual.genotype[index] ^= 1

    def two_point_mutation(self, individual: 'Individual'):
        if self.should_mutate():
            idx1, idx2 = random.sample(range(len(individual.genotype)), 2)
            individual.genotype[idx1] ^= 1
            individual.genotype[idx2] ^= 1

    def softmax_mutation(self, individual: 'Individual'):
        values = np.array(individual.genotype, dtype=np.float32)
        exp_values = np.exp(values - np.max(values))
        probabilities = exp_values / np.sum(exp_values)
        
        for i in range(len(individual.genotype)):
            if random.random() < probabilities[i] * self.mutation_rate:
                individual.genotype[i] ^= 1

    def lambda_mutation(self, individual: 'Individual'):
        if self.should_mutate():
            chaotic_index = int((math.sin(random.random()) + 1) / 2 * (len(individual.genotype) - 1))
            individual.genotype[chaotic_index] ^= 1

    def jumping_gene_mutation(self, individual: 'Individual'):
        if self.should_mutate():
            index1, index2 = random.sample(range(len(individual.genotype)), 2)
            individual.genotype[index1], individual.genotype[index2] = (
                individual.genotype[index2], individual.genotype[index1]
            )

    def inversion(self, individual: 'Individual'):
        if self.should_mutate():
            idx1, idx2 = sorted(random.sample(range(len(individual.genotype)), 2))
            individual.genotype[idx1:idx2 + 1] = reversed(individual.genotype[idx1:idx2 + 1])
