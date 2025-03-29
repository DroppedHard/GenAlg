from app.algorithms.crossovers import Crossover
from app.algorithms.mutation import Mutation
from app.algorithms.selections import Selection
from app.representation.individual import Individual


class Simulation:
    def __init__(self, selection: Selection, crossover: Crossover, mutation: Mutation):
        self.epoch = 1000
        self.dest_function = lambda x: x**2
        self.limit = (-2, 2)
        self.population_size = 100
        self.selection: Selection = selection
        self.crossover: Crossover = crossover
        self.mutation: Mutation = mutation

    def initializePopulation(self) -> list[Individual]:
        pass

    def run(self):
        """Rozpoczęcie symulacji"""
        population = self.initializePopulation()
        for _ in range(self.epoch):
            # evaluate
            # te poniżej to przykładowo jak to ma iść - tutaj możecie dostosować do tego co chcecie
            selected = self.selection.select(population)
            self.crossover.crossover_population(selected)
            self.mutation.mutate()  # wiem że teraz nie zadziała - wymaga refactoringu

        # TODO print results
