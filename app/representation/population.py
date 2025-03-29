from app.representation.individual import Individual
from typing import Literal


class Population:
    def __init__(
        self,
        a: int,
        b: int,
        func,
        n_of_variables: int,
        chrom_length: int,
        population_size: int,
        epochs: int,
        optimization_type: Literal["min", "max"],
        best_indv_number: int,
    ):
        self.a = a
        self.b = b
        self.func = func
        self.n_of_variables = n_of_variables
        self.chrom_length = chrom_length
        self.population_size = population_size
        self.epochs = epochs
        self.optimization_type = optimization_type
        self.best_indv_number = best_indv_number
        self.population = self.create_population() 

    def create_population(self):
        return [
            Individual(
                self.a, self.b, self.func, self.chrom_length, self.n_of_variables
            )
            for _ in range(self.population_size)
        ]

    def sort_population(self):
        reverse_sort = self.optimization_type == "max"
        self.population = sorted(
            self.population,
            key=lambda ind: ind.target_function_val,
            reverse=reverse_sort,
        )

    def new_population(self, new_population):
        self.population = new_population

    def get_best_individuals(self):
        """
        To be used after selection and setting new population to get the best individuals.
        Warning: after this function is called, the population is sorted.
        """
        self.sort_population()
        self.elitary_population = self.population[: self.best_indv_number]
        return self.elitary_population
