from app.algorithms.crossovers import Crossover
from app.algorithms.mutation import Inversion, Mutation
from app.algorithms.selections import Selection
from app.representation.individual import Individual
from app.representation.population import Population

from pathlib import Path


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
        self.simulation_is_running = False
    
    def create_file(self) -> Path:
        base_dir = Path(__file__).resolve().parent.parent
        file_path = base_dir / "results" / f"test.txt"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        file_path.write_text(
            f"{self.epochs}\n{self.mutation.getName()}\n{self.crossover.getName()}\n{self.selection.getName()}",
            encoding="utf-8",
        )
        return file_path
    
    def get_statistics(self):
        if self.simulation_is_running:
            return "Simulation is running"
        return self.target_functions


    def run(self):
        """Rozpoczęcie symulacji"""

        print("ZACZYNAMY")
        self.target_functions = []
        file_path = self.create_file()
        self.simulation_is_running = True
        for epoch in range(self.epochs):
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

            self.target_functions.append(best_individuals[0].target_function_val)
            avg_target_function = sum(
                [ind.target_function_val for ind in self.population.population]
            ) / len(self.population.population)

            standard_deviation = (
                sum(
                    (ind.target_function_val - avg_target_function) ** 2
                    for ind in self.population.population
                )
                / len(self.population.population)
            ) ** 0.5

            self.target_functions.append((best_individuals[0].target_function_val, avg_target_function, standard_deviation))

            with file_path.open("a", encoding="utf-8") as f:
                f.write(f"{epoch + 1} {best_individuals[0].target_function_val} {avg_target_function} {standard_deviation} \n")

        self.simulation_is_running = False
        print("KONIEC")
        print("Populacja:")
        print(self.population.population)
        print("Najlepsi osobnicy:")
        print(self.population.get_best_individuals())


        # # TODO print results
