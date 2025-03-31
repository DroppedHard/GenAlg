from app.algorithms.crossovers import Crossover
from app.algorithms.mutation import Inversion, Mutation
from app.algorithms.selections import Selection
from app.representation.individual import Individual
from app.representation.population import Population


class Simulation:
    def __init__(
        self,
        epochs: int,
        population: Population,
        inversion: Inversion,
        mutation: Mutation,
        selection: Selection,
        crossover: Crossover,
    ):
        if epochs < 0:
            raise ValueError(f"Liczba epok musi być dodatnia, a nie równa {epochs}")
        self.epochs = epochs
        self.population = population
        self.inversion = inversion
        self.mutation = mutation
        self.selection = selection
        self.crossover = crossover

    def run(self):
        """Rozpoczęcie symulacji"""

        print("ZACZYNAMY")
        for _ in range(self.epochs):
            individuals = self.population.population
            selected = self.selection.select(individuals)
            self.population.new_population(selected)
            best_individuals = self.population.get_best_individuals()
            pop_after_crossed = self.crossover.crossover_population(
                selected, best_individuals
            )
            mutated = list(
                map(lambda ind: self.mutation.mutate(ind), pop_after_crossed)
            )
            inversed = list(map(lambda ind: self.inversion.inverse(ind), mutated))
            self.population.new_population(inversed)

        print("KONIEC")
        print("Populacja:")
        print(self.population.population)
        print("Najlepsi osobnicy:")
        print(self.population.get_best_individuals())

        # # TODO print results
