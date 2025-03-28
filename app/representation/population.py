from app.representation.individual import Individual
from typing import Literal


class Population:
    def __init__(self, a:int, b:int, func, n_of_variables:int, chrom_length:int, population_size:int, epochs:int, optimization_type:Literal["min", "max"]):
        self.a = a
        self.b = b
        self.func = func
        self.n_of_variables = n_of_variables
        self.chrom_length = chrom_length
        self.population_size = population_size
        self.epochs = epochs
        self.optimization_type = optimization_type
        self.population = self.create_population()

    def create_population(self):
        return [Individual(self.a, self.b, self.func, self.chrom_length, self.n_of_variables) for _ in range(self.population_size)]
    
    def sort_population(self):
        reverse_sort = self.optimization_type == "max"
        self.population = sorted(self.population, key=lambda ind: ind.target_function_val, reverse=reverse_sort)
