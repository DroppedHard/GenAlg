from app.representation.population import Population
from app.representation.individual import Individual
import math
import random
from typing import List


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
        for chromosome in individual.chromosomes:
            if self.should_mutate():
                if random.random() < 0.5:
                    chromosome.gens[0] ^= 1
                else:
                    chromosome.gens[-1] ^= 1
        return individual

class SinglePointMutation(Mutation):
    def getName() -> str:
        return "Mutacja Jednopunktowa"

    def mutate(self, individual: Individual):
        for chromosome in individual.chromosomes:
            if self.should_mutate():
                index = random.randint(0, len(chromosome.gens) - 1)
                chromosome.gens[index] ^= 1
        return individual


class TwoPointMutation(Mutation):
    def getName() -> str:
        return "Mutacja Dwupunktowa"

    def mutate(self, individual: Individual):
        for chromosome in individual.chromosomes:
            if self.should_mutate():
                idx1, idx2 = random.sample(range(len(individual.chromosomes)), 2)
                chromosome.gens[idx1] ^= 1
                chromosome.gens[idx2] ^= 1
        return individual

class Inversion:
    def __init__(self, probability: float = 0.1):
        if not (0 <= probability <= 1):
            raise ValueError("probability must be between 0 and 1")
        self.probability = probability

    def should_apply(self) -> bool:
        return random.random() < self.probability

    def apply(self, individual: Individual):
        if self.should_apply():
            idx1, idx2 = sorted(random.sample(range(len(individual.chromosomes)), 2))
            individual.chromosomes[idx1 : idx2 + 1] = reversed(
                individual.chromosomes[idx1 : idx2 + 1]
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
