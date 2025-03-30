from app.algorithms.crossovers import Crossover
from app.algorithms.mutation import Inversion, Mutation
from app.algorithms.selections import Selection
from app.representation.individual import Individual
from app.representation.population import Population


class Simulation:
    def __init__(
        self,
        objective_function,
        epochs: int,
        limit: tuple[int],
        population_size: int,
        n_of_variables: int,
        chrom_length: int,
        precision: float,
        optimization_type: str,
        best_indv_number: int,
        inversion: Inversion,
        mutation: Mutation,
        selection: Selection,
        crossover: Crossover,
    ):
        self.epochs = epochs
        self.objective_function = objective_function
        self.limit = limit
        self.population_size = population_size
        self.n_of_variables = n_of_variables
        self.chrom_length = chrom_length
        self.precision = precision
        self.optimization_type = optimization_type
        self.best_indv_number = best_indv_number
        self.inversion = inversion
        self.mutation = mutation
        self.selection = selection
        self.crossover = crossover

    def initializePopulation(self) -> None:
        func = lambda x, y, z: x**2 + y**2 + z**2  # Przykładowa funkcja celu
        self.population = Population(
            self.limit[0],
            self.limit[1],
            func,
            self.n_of_variables,
            self.chrom_length,
            self.population_size,
            self.precision,
            self.optimization_type,
            self.best_indv_number,
        )
        return self.population.population

    def run(self):
        """Rozpoczęcie symulacji"""

        print("ZACZYNAMY")
        self.initializePopulation()
        for _ in range(self.epochs):
            individuals = self.population.population
            selected = self.selection.select(individuals)
            self.population.new_population(selected)
            best_individuals = self.population.get_best_individuals()
            pop_after_crossed = self.crossover.crossover_population(selected, best_individuals)
            mutated = list(map(lambda ind: self.mutation.mutate(ind), pop_after_crossed))
            inversed = self.inversion.inverse(mutated)
            self.population.new_population(inversed)



        print("KONIEC")
        print("Populacja:")
        print(self.population.population)
        print("Najlepsi osobnicy:")
        print(self.population.get_best_individuals())

        # # TODO print results
