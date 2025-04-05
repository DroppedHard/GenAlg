from app.algorithms.crossovers import Crossover
from app.algorithms.mutation import Inversion, Mutation
from app.algorithms.selections import Selection
from app.representation.individual import Individual
from app.representation.population import Population

from pathlib import Path
import datetime


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
    
    def create_file(self) -> Path:
        base_dir = Path(__file__).resolve().parent.parent
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = base_dir / "results" / f"{timestamp}.txt"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(
            f"{self.epochs} {self.mutation.getName()} {self.crossover.getName()} {self.selection.getName()}\n"
            )
            f.write(
            f"{self.population.a} {self.population.b} {self.population.optimization_type} \n"
            )
        return file_path
    
    def get_statistics(self):
        return self.target_functions, self.duration_time


    def run(self):
        """Rozpoczęcie symulacji"""
        start_time = datetime.datetime.now()
        self.target_functions = []
        file_path = self.create_file()
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

            self.target_functions.append((epoch+1, best_individuals[0].decodes, best_individuals[0].target_function_val, avg_target_function, standard_deviation))

            with file_path.open("a", encoding="utf-8") as f:
                f.write(f"{epoch + 1} {best_individuals[0].target_function_val} {avg_target_function} {standard_deviation} \n")
        end_time = datetime.datetime.now()
        self.duration_time = end_time - start_time