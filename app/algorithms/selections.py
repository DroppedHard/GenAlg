from app.representation.population import Population
from app.representation.individual import Individual
import math
import random
from typing import List, Literal, Tuple


class Selection:
    def __init__(self):
        pass

    @staticmethod
    def getName() -> str:
        pass

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        pass

    @staticmethod
    def validateParameters() -> bool:
        pass

    def select(self) -> List[Individual]:
        pass


class SelectionTheBest(Selection):
    def __init__(self, percentage: int, optimization_type: Literal["min", "max"]):
        self.optimization_type = optimization_type
        self.percentage = percentage

    @staticmethod
    def getName():
        return "Selekcja części najlepszych"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("Procent najlepszych", "10"), ("Typ optymalizacji", "min")]

    @staticmethod
    def validateParameters(
        percentage: int, optimization_type: Literal["min", "max"]
    ) -> bool:
        if 0 < percentage < 100 and optimization_type in ["min", "max"]:
            return True
        return False

    def select(self, population: list[Individual]) -> List[Individual]:
        pass
        # i tutaj wykonujemy to sortowanie i zwracamy top jakiś % albo top liczba - do dogadania
        reverse_sort = self.optimization_type == "max"
        population = sorted(
            population,
            key=lambda ind: ind.target_function_val,
            reverse=reverse_sort,
        )
        n_to_select = math.ceil(len(population) * self.percentage / 100)
        return population[:n_to_select]


class TournamentSelection(Selection):
    def __init__(
        self,
        tournament_capacity: int,
        tournament_count: int,
        optimization_type: Literal["min", "max"],
    ):
        self.optimization_type = optimization_type
        self.tournament_capacity = tournament_capacity
        self.tournament_count = tournament_count

    @staticmethod
    def getName():
        return "Selekcja turniejowa"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [
            ("Ilośc turniejów", "3"),
            ("Ilość osobników w grupie", "4"),
            ("Typ optymalizacji", "min"),
        ]

    @staticmethod
    def validateParameters(
        tournament_count: int,
        tournament_capacity: int,
        optimization_type: Literal["min", "max"],
    ) -> bool:
        if (
            tournament_count < 0
            or tournament_capacity < 0
            or optimization_type not in ["min", "max"]
        ):
            return False
        return True

    def select(self, population: List[Individual]) -> List[Individual]:
        length = len(population)
        chunks = [
            population[i : i + self.tournament_capacity]
            for i in range(0, length, self.tournament_capacity)
        ]
        for tornament in range(self.tournament_count):
            selected = []
            for chunk in chunks:
                reverse_sort = self.optimization_type == "max"
                chunk = sorted(
                    chunk, key=lambda ind: ind.target_function_val, reverse=reverse_sort
                )
                selected.append(chunk[0])
            length = len(selected)
            chunks = [
                selected[i : i + self.tournament_capacity]
                for i in range(0, length, self.tournament_capacity)
            ]
        return selected


class RouletteWheelSelection(Selection):
    def __init__(self, n_to_select: int, optimization_type: Literal["min", "max"]):
        self.n_to_select = n_to_select
        self.optimization_type = optimization_type

    @staticmethod
    def getName():
        return "Selekcja koła fortuny"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("Liczba osobników do wytypowania", "5"), ("Typ optymalizacji", "min")]

    @staticmethod
    def validateParameters(
        n_to_select: int, optimization_type: Literal["min", "max"]
    ) -> bool:
        if n_to_select < 0 or optimization_type not in ["min", "max"]:
            return False
        return True

    def calculate_distribution(self, target_function_vals: List[float]) -> List[float]:
        if self.optimization_type == "max":
            val_sum = sum(target_function_vals)
            probability = [val / val_sum for val in target_function_vals]
        else:
            target_function_vals = [1 / val for val in target_function_vals]
            val_sum = sum(target_function_vals)
            probability = [val / val_sum for val in target_function_vals]

        distribution = [sum(probability[: i + 1]) for i in range(len(probability))]
        return distribution

    def select(self, population: List[Individual]) -> List[Individual]:
        target_function_vals = [idv.target_function_val for idv in population]

        minimum = min(target_function_vals)
        epsilon = 0.0000001

        if minimum <= 0:
            target_function_vals = [
                val + abs(minimum) + epsilon for val in target_function_vals
            ]

        distribution = self.calculate_distribution(target_function_vals)

        rand = random.random()
        selected_numbers = []
        selected = []
        j = 0

        while j < self.n_to_select:
            for i in range(len(distribution)):
                rand = random.random()
                if rand < distribution[i]:
                    if i not in selected_numbers:
                        selected.append(population[i])
                        selected_numbers.append(i)
                        j += 1
                        break

        return selected


AVAILABLE_SELECTIONS: List[Selection] = [
    SelectionTheBest,
    TournamentSelection,
    RouletteWheelSelection,
]
