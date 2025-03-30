from app.representation.population import Population
from app.representation.individual import Individual
import math
import random
from typing import List

# import numpy as np


class Mutation:
    def __init__(self, mutation_rate: float = 0.1):
        if not (0 <= mutation_rate <= 1):
            raise ValueError("mutation_rate must be between 0 and 1")
        self.mutation_rate = mutation_rate

    @staticmethod
    def getName() -> str:
        pass

    def should_mutate(self) -> bool:
        return random.random() < self.mutation_rate

    def mutate(self, individual: Individual):
        pass


class BoundaryMutation(Mutation):
    @staticmethod
    def getName() -> str:
        return "Mutacja Brzegowa"

    def mutate(self, individual: Individual):
        if self.should_mutate():
            if random.random() < 0.5:
                individual.genotype[0] ^= 1
            else:
                individual.genotype[-1] ^= 1


class SinglePointMutation(Mutation):
    def getName() -> str:
        return "Mutacja Jednopunktowa"

    def mutate(self, individual: Individual):
        if self.should_mutate():
            index = random.randint(0, len(individual.genotype) - 1)
            individual.genotype[index] ^= 1


class TwoPointMutation(Mutation):
    def getName() -> str:
        return "Mutacja Dwupunktowa"

    def mutate(self, individual: Individual):
        if self.should_mutate():
            idx1, idx2 = random.sample(range(len(individual.genotype)), 2)
            individual.genotype[idx1] ^= 1
            individual.genotype[idx2] ^= 1


"""
class SoftmaxMutation(Mutation):
    def mutate(self, individual: Individual):
        values = individual.genotype
        max_value = max(values)
        exp_values = [math.exp(v - max_value) for v in values]
        sum_exp_values = sum(exp_values)
        probabilities = [ev / sum_exp_values for ev in exp_values]

        for i in range(len(individual.genotype)):
            if random.random() < probabilities[i] * self.mutation_rate:
                individual.genotype[i] ^= 1

class LambdaMutation(Mutation):
    def mutate(self, individual: Individual):
        if self.should_mutate():
            chaotic_index = int(
                (math.sin(random.random()) + 1) / 2 * (len(individual.genotype) - 1)
            )
            individual.genotype[chaotic_index] ^= 1

class JumpingGeneMutation(Mutation):
    def mutate(self, individual: Individual):
        if self.should_mutate():
            index1, index2 = random.sample(range(len(individual.genotype)), 2)
            individual.genotype[index1], individual.genotype[index2] = (
                individual.genotype[index2],
                individual.genotype[index1],
            )
"""


class Inversion:
    def __init__(self, probability: float = 0.1):
        if not (0 <= probability <= 1):
            raise ValueError("probability must be between 0 and 1")
        self.probability = probability

    def should_apply(self) -> bool:
        return random.random() < self.probability

    def apply(self, individual: Individual):
        if self.should_apply():
            idx1, idx2 = sorted(random.sample(range(len(individual.genotype)), 2))
            individual.genotype[idx1 : idx2 + 1] = reversed(
                individual.genotype[idx1 : idx2 + 1]
            )


def inversion(population: "Population") -> "Population":
    inversion_operator = Inversion()
    for individual in population.population:
        inversion_operator.apply(individual)
    return population


AVAILABLE_MUTATIONS: List[Mutation] = [
    BoundaryMutation,
    SinglePointMutation,
    TwoPointMutation,
]
