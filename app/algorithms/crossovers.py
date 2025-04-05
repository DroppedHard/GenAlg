import random
from app.representation.individual import Individual
from app.representation.chromosome import Chromosome
from app.representation.population import Population
from typing import List, Tuple
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

    def crossover_population(self, population: List[Individual], best_indviduals: List[Individual]) -> list[Individual]:
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
        return [("rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(whole_pop_size: int) -> bool:
        if whole_pop_size < 0:
            return False
        return True

    def crossover(self) -> list[Individual]:
        point = random.randint(1, self.parent1.length - 1)
        base = list(zip(self.parent1.chromosomes, self.parent2.chromosomes))

        child1_chromosomes = [Chromosome(pair[0].length, pair[0].gens[:point] + pair[1].gens[point:]) for pair in base]
        child2_chromosomes = [Chromosome(pair[0].length, pair[0].gens[point:] + pair[1].gens[:point]) for pair in base]

        child1 = Individual(parent = self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent = self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]
    
class TwoPointCrossover(Crossover):
    def __init__(self, whole_pop_size: int) -> None:
        self.whole_pop_size = whole_pop_size

    @staticmethod
    def getName() -> str:
        return "Krzyżowanie dwupunktowe"

    @staticmethod
    def getParamteres() -> List[Tuple[str]]:
        return [("rozmiar populacji", "50")]

    @staticmethod
    def validateParameters(whole_pop_size) -> bool:
        if whole_pop_size < 0:
            return False
        return True
    
    def crossover(self) -> list[Individual]:
        point1 = random.randint(1, self.parent1.length - 2)
        point2 = random.randint(point1 + 1, self.parent1.length - 1)

        base = list(zip(self.parent1.chromosomes, self.parent2.chromosomes))

        child1_chromosomes = [Chromosome(pair[0].length, pair[0].gens[:point1] + pair[1].gens[point1:point2] + pair[0].gens[point2:]) for pair in base]
        child2_chromosomes = [Chromosome(pair[1].length, pair[1].gens[:point1] + pair[0].gens[point1:point2] + pair[1].gens[point2:]) for pair in base]

        child1 = Individual(parent = self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent = self.parent2, chromosomes=child2_chromosomes)
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
        return [("prawdopodobieństwo", "0.5"), ("rozmiar populacji", "50")]

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
        child1 = Individual(parent = self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent = self.parent2, chromosomes=child2_chromosomes)
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
        return [("prawdopodobieństwo", "0.5"), ("rozmiar populacji", "50")]

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
        child = Individual(parent = self.parent1, chromosomes=child_chromosomes)
        return [child]   


AVAILABLE_CROSSOVERS: List[Crossover] = [
    SinglePointCrossover,
    TwoPointCrossover,
    UniformCrossover,
    DiscreteCrossover,
]
