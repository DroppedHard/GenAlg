from app.representation.population import Population
from app.representation.individual import Individual
import math
import random
from typing import List

class Selection():
    def __init__(self, population: Population, n_to_select: int):
        self.population = population
        self.n_to_select = n_to_select
        if n_to_select < 0 or n_to_select > self.population.population_size:
            raise ValueError("n_to_select must be between 0 and population size")

    def select(self):
        pass

class SelectionTheBest(Selection):
    def __init__(self, population: Population, n_to_select: int):
        super().__init__(population, n_to_select)

    def select(self) -> List[Individual]:
        self.population.sort_population()
        return self.population.population[:self.n_to_select]

class TournamentSelection(Selection):
    def __init__(self, population: Population, n_to_select: int):
        super().__init__(population, n_to_select)
        self.k = math.ceil(self.population.population_size / self.n_to_select)


    def select(self) -> List[Individual]:
        length = self.population.population_size
        individuals = self.population.population
        chunks = [individuals[i:i + self.k] for i in range(0, length, self.k)]
        selected =[]
        for chunk in chunks:
            reverse_sort = self.population.optimization_type == "max"
            chunk = sorted(chunk, key=lambda ind: ind.target_function_val, reverse=reverse_sort)
            selected.append(chunk[0])
        return selected

class RouletteWheelSelection(Selection):
    def __init__(self, population: Population, n_to_select: int):
        super().__init__(population, n_to_select)

    def calculate_distribution(self, target_function_vals: List[float], optimization_type: str) -> List[float]:
        if optimization_type == "max":
            val_sum = sum(target_function_vals)
            probability = [val / val_sum for val in target_function_vals]
        else:
            target_function_vals = [1 / val for val in target_function_vals]
            val_sum = sum(target_function_vals)
            probability = [val / val_sum for val in target_function_vals]

        distribution = [sum(probability[:i + 1]) for i in range(len(probability))]
        return distribution

    def select(self) -> List[Individual]:
        individuals = self.population.population
        target_function_vals = [idv.target_function_val for idv in individuals]

        minimum = min(target_function_vals)
        epsilon = 0.0000001

        if minimum <= 0:
            target_function_vals = [val + abs(minimum) + epsilon for val in target_function_vals]

        distribution = self.calculate_distribution(target_function_vals, self.population.optimization_type)

        rand = random.random()
        selected_numbers = []
        selected = []
        j = 0

        while j < self.n_to_select:
            for i in range(len(distribution)):
                rand = random.random()
                if rand < distribution[i]:
                    if i not in selected_numbers:
                        selected.append(individuals[i])
                        selected_numbers.append(i)
                        j += 1
                        break

        return selected
        