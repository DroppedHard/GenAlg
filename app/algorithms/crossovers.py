import random
from app.representation.individual import Individual
from app.representation.chromosome import Chromosome
from app.representation.population import Population
from typing import List, Tuple, Literal
from copy import deepcopy


class Crossover:
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

    def crossover(self) -> List[Individual]:
        pass

    def get_parents(self) -> None:
        self.parent1: Individual = random.choice(self.population)
        self.parent2: Individual = random.choice(self.population)

    def validate_real_values(self, child) -> None:
        for val in child.real_values:
            if val < child.a or val > child.b:
                return False
        return True

    def crossover_population(
        self, population: List[Individual], best_indviduals: List[Individual]
    ) -> list[Individual]:
        self.population = population

        size = self.whole_pop_size - len(best_indviduals)
        actual_size = 0
        new_population = deepcopy(best_indviduals)
        while actual_size < size:
            self.get_parents()
            children = self.crossover()
            if actual_size + len(children) > size:
                child_number = random.randint(1, len(children))
                children = children[:child_number]
            for child in children:
                new_population.append(child)
                actual_size += 1
        return new_population


class SinglePointCrossover(Crossover):
    def __init__(self, whole_pop_size: int) -> None:
        self.whole_pop_size = whole_pop_size

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie jednopunktowe"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("Rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(whole_pop_size: int) -> bool:
        if whole_pop_size < 0:
            return False
        return True

    def crossover(self) -> list[Individual]:
        point = random.randint(1, self.parent1.length - 1)
        base = list(zip(self.parent1.chromosomes, self.parent2.chromosomes))

        child1_chromosomes = [
            Chromosome(pair[0].length, pair[0].gens[:point] + pair[1].gens[point:])
            for pair in base
        ]
        child2_chromosomes = [
            Chromosome(pair[0].length, pair[0].gens[point:] + pair[1].gens[:point])
            for pair in base
        ]

        child1 = Individual(parent=self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent=self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]


class TwoPointCrossover(Crossover):
    def __init__(self, whole_pop_size: int) -> None:
        self.whole_pop_size = whole_pop_size

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie dwupunktowe"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("Rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(whole_pop_size) -> bool:
        if whole_pop_size < 0:
            return False
        return True

    def crossover(self) -> list[Individual]:
        point1 = random.randint(1, self.parent1.length - 2)
        point2 = random.randint(point1 + 1, self.parent1.length - 1)

        base = list(zip(self.parent1.chromosomes, self.parent2.chromosomes))

        child1_chromosomes = [
            Chromosome(
                pair[0].length,
                pair[0].gens[:point1]
                + pair[1].gens[point1:point2]
                + pair[0].gens[point2:],
            )
            for pair in base
        ]
        child2_chromosomes = [
            Chromosome(
                pair[1].length,
                pair[1].gens[:point1]
                + pair[0].gens[point1:point2]
                + pair[1].gens[point2:],
            )
            for pair in base
        ]

        child1 = Individual(parent=self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent=self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]


class UniformCrossover(Crossover):
    def __init__(self, probability: float, whole_pop_size: int) -> None:
        self.probability = probability
        self.whole_pop_size = whole_pop_size

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie jednorodne"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("prawdopodobieństwo", "0.5"), ("Rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(probability: float, whole_pop_size: int) -> bool:
        if probability < 0 or probability > 1 or whole_pop_size < 0:
            return False
        return True

    def crossover(self) -> list[Individual]:
        child1_chromosomes = []
        child2_chromosomes = []
        base = list(zip(self.parent1.chromosomes, self.parent2.chromosomes))
        for pair in base:
            child1_chromosome = []
            child2_chromosome = []
            for i in range(self.parent1.length):
                if random.random() < self.probability:
                    child1_chromosome.append(pair[0].gens[i])
                    child2_chromosome.append(pair[1].gens[i])
                else:
                    child1_chromosome.append(pair[1].gens[i])
                    child2_chromosome.append(pair[0].gens[i])
            child1_chromosomes.append(Chromosome(pair[0].length, child1_chromosome))
            child2_chromosomes.append(Chromosome(pair[1].length, child2_chromosome))
        child1 = Individual(parent=self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent=self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]


class DiscreteCrossover(Crossover):
    def __init__(self, probability: float, whole_pop_size: int) -> None:
        self.probability = probability
        self.whole_pop_size = whole_pop_size

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie ziarniste"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("prawdopodobieństwo", "0.5"), ("Rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(probability: float, whole_pop_size: int) -> bool:
        if probability < 0 or probability > 1 or whole_pop_size < 0:
            return False
        return True

    def crossover(self) -> list[Individual]:
        child_chromosomes = []
        base = list(zip(self.parent1.chromosomes, self.parent2.chromosomes))
        for pair in base:
            child_chromosome = []
            for i in range(self.parent1.length):
                if random.random() < self.probability:
                    child_chromosome.append(pair[0].gens[i])
                else:
                    child_chromosome.append(pair[1].gens[i])
            child_chromosomes.append(Chromosome(pair[0].length, child_chromosome))
        child = Individual(parent=self.parent1, chromosomes=child_chromosomes)
        return [child]


class ArithmeticalCrossover(Crossover):
    def __init__(self, probability: float, whole_pop_size: int) -> None:
        self.probability = probability
        self.whole_pop_size = whole_pop_size

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie arytmetyczne"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("prawdopodobieństwo", "0.5"), ("Rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(probability: float, whole_pop_size: int) -> bool:
        if probability < 0 or probability > 1 or whole_pop_size < 0:
            return False
        return True

    def crossover(self) -> list[Individual]:
        alpha = random.uniform(0, 1)
        all_children_valid = False
        while not all_children_valid:
            child1_val = []
            child2_val = []
            for val1, val2 in zip(self.parent1.real_values, self.parent2.real_values):
                child1_val.append(alpha * val1 + (1 - alpha) * val2)
                child2_val.append((1 - alpha) * val1 + alpha * val2)
            child1 = Individual(
                parent=self.parent1, real_values=child1_val, real_representation=True
            )
            child2 = Individual(
                parent=self.parent2, real_values=child2_val, real_representation=True
            )
            all_children_valid = self.validate_real_values(
                child1
            ) and self.validate_real_values(child2)

        return [child1, child2]


class LinearCrossover(Crossover):
    def __init__(
        self,
        probability: float,
        whole_pop_size: int,
        optimization_type: Literal["min", "max"],
    ) -> None:
        self.probability = probability
        self.whole_pop_size = whole_pop_size
        self.optimization_type = optimization_type

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie linearne"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [
            ("prawdopodobieństwo", "0.5"),
            ("Rozmiar populacji", "50"),
            ("Typ optymalizacji", "min"),
        ]

    @staticmethod
    def validateParameters(
        probability: float,
        whole_pop_size: int,
        optimization_type: Literal["min", "max"],
    ) -> bool:
        if (
            probability < 0
            or probability > 1
            or whole_pop_size < 0
            or optimization_type not in ["min", "max"]
        ):
            return False
        return True

    def crossover(self) -> list[Individual]:
        const1 = 1 / 2
        const2 = 3 / 2
        child1_val = []
        child2_val = []
        child3_val = []
        for val1, val2 in zip(self.parent1.real_values, self.parent2.real_values):
            child1_val.append(const1 * val1 + const1 * val2)
            child2_val.append(const2 * val1 - const1 * val2)
            child3_val.append(-const1 * val1 + const2 * val2)

        child1 = Individual(
            parent=self.parent1, real_values=child1_val, real_representation=True
        )
        child2 = Individual(
            parent=self.parent2, real_values=child2_val, real_representation=True
        )
        child3 = Individual(
            parent=self.parent1, real_values=child3_val, real_representation=True
        )
        get_children = [child1, child2, child3]
        get_valid_children = [
            child for child in get_children if self.validate_real_values(child)
        ]

        if len(get_valid_children) > 2:
            get_valid_children.sort(
                key=lambda x: x.target_function_val,
                reverse=(True if self.optimization_type == "max" else False),
            )
            return get_valid_children[:2]

        return get_valid_children


class AlfaMixCrossover(Crossover):
    def __init__(self, probability: float, whole_pop_size: int, alpha: float) -> None:
        self.probability = probability
        self.whole_pop_size = whole_pop_size
        self.alpha = alpha

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie Alfa Mieszające"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [
            ("prawdopodobieństwo", "0.5"),
            ("Rozmiar populacji", "50"),
            ("Parametr alfa", "0.5"),
        ]

    @staticmethod
    def validateParameters(
        probability: float, whole_pop_size: int, alpha: float
    ) -> bool:
        if (
            probability < 0
            or probability > 1
            or whole_pop_size < 0
            or alpha < 0
            or alpha > 1
        ):
            return False
        return True

    def crossover(self) -> list[Individual]:
        child1_val = []
        child2_val = []
        all_children_valid = False
        while not all_children_valid:
            child1_val = []
            child2_val = []
            for val1, val2 in zip(self.parent1.real_values, self.parent2.real_values):
                d = abs(val1 - val2)
                values = [
                    min(val1, val2) - self.alpha * d,
                    max(val1, val2) + self.alpha * d,
                ]
                child1_val.append(random.uniform(values[0], values[1]))
                child2_val.append(random.uniform(values[0], values[1]))
            child1 = Individual(
                parent=self.parent1, real_values=child1_val, real_representation=True
            )
            child2 = Individual(
                parent=self.parent2, real_values=child2_val, real_representation=True
            )
            all_children_valid = self.validate_real_values(
                child1
            ) and self.validate_real_values(child2)
        return [child1, child2]


class AlfaAndBetaMixCrossover(Crossover):
    def __init__(
        self, probability: float, whole_pop_size: int, alpha: float, beta: float
    ) -> None:
        self.probability = probability
        self.whole_pop_size = whole_pop_size
        self.alpha = alpha
        self.beta = beta

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie Alfa i Beta Mieszające"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [
            ("prawdopodobieństwo", "0.5"),
            ("Rozmiar populacji", "50"),
            ("Parametr alfa", "0.5"),
            ("Parametr beta", "0.5"),
        ]

    @staticmethod
    def validateParameters(
        probability: float, whole_pop_size: int, alpha: float, beta: float
    ) -> bool:
        if (
            probability < 0
            or probability > 1
            or whole_pop_size < 0
            or alpha < 0
            or alpha > 1
            or beta < 0
            or beta > 1
        ):
            return False
        return True

    def crossover(self) -> list[Individual]:
        child1_val = []
        child2_val = []
        all_children_valid = False
        while not all_children_valid:
            child1_val = []
            child2_val = []
            for val1, val2 in zip(self.parent1.real_values, self.parent2.real_values):
                d = abs(val1 - val2)
                values = [
                    min(val1, val2) - self.alpha * d,
                    max(val1, val2) + self.beta * d,
                ]
                child1_val.append(random.uniform(values[0], values[1]))
                child2_val.append(random.uniform(values[0], values[1]))
            child1 = Individual(
                parent=self.parent1, real_values=child1_val, real_representation=True
            )
            child2 = Individual(
                parent=self.parent2, real_values=child2_val, real_representation=True
            )
            all_children_valid = self.validate_real_values(
                child1
            ) and self.validate_real_values(child2)
        return [child1, child2]


class AverageCrossover(Crossover):
    def __init__(self, probability: float, whole_pop_size: int) -> None:
        self.probability = probability
        self.whole_pop_size = whole_pop_size

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie uśredniające"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("prawdopodobieństwo", "0.5"), ("Rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(probability: float, whole_pop_size: int) -> bool:
        if probability < 0 or probability > 1 or whole_pop_size < 0:
            return False
        return True

    def crossover(self) -> list[Individual]:
        child1_val = []
        for val1, val2 in zip(self.parent1.real_values, self.parent2.real_values):
            child1_val.append((val1 + val2) / 2)
        child1 = Individual(
            parent=self.parent1, real_values=child1_val, real_representation=True
        )
        return [child1]


AVAILABLE_CROSSOVERS: List[Crossover] = [
    SinglePointCrossover,
    TwoPointCrossover,
    UniformCrossover,
    DiscreteCrossover,
]

# TBD: Add real representation crossovers
REAL_REPRESENTATION_CROSSOVERS: List[Crossover] = [
    ArithmeticalCrossover,
    LinearCrossover,
    AlfaMixCrossover,
    AlfaAndBetaMixCrossover,
    AverageCrossover,
]
