from app.algorithms.crossovers import Crossover
from app.algorithms.mutation import Inversion, Mutation
from app.algorithms.selections import Selection
from app.representation.individual import Individual


class Simulation:
    def __init__(
        self,
        objective_function,
        epochs: int,
        limit: tuple[int],
        inversion: Inversion,
        mutation: Mutation,
        selection: Selection,
        crossover: Crossover,
    ):
        self.epochs = epochs
        self.objective_function = objective_function
        self.limit = limit
        self.inversion = inversion
        self.mutation = mutation
        self.selection = selection
        self.crossover = crossover

    def initializePopulation(self) -> list[Individual]:
        pass

    def run(self):
        """Rozpoczęcie symulacji"""
        print("ZACZYNAMY")
        # population = self.initializePopulation()
        # for _ in range(self.epochs):
        #     # evaluate
        #     # te poniżej to przykładowo jak to ma iść - tutaj możecie dostosować do tego co chcecie
        #     selected = self.selection.select(population)
        #     self.crossover.crossover_population(selected)
        #     self.mutation.mutate()  # wiem że teraz nie zadziała - wymaga refactoringu

        # # TODO print results
