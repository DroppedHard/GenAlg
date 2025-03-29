import random
from app.representation.individual import Individual
from app.representation.population import Population

class Crossover:
    def __init__(self, population: list[Individual], best_indviduals: list[Individual], whole_pop_size: int) -> None:
        self.population: list[Individual] = population
        self.best_indviduals: list[Individual] = best_indviduals
        self.whole_pop_size: int = whole_pop_size

    def get_parents(self) -> None:
        self.parent1 = random.choice(self.population)
        self.parent2 = random.choice(self.population)
        while self.parent1 == self.parent2:
            self.parent2 = random.choice(self.population)

    def crossover(self):
        raise NotImplementedError("Crossover method not implemented.")
    
    def crossover_population(self) -> list[Individual]:
        size = self.whole_pop_size - len(self.best_indviduals)
        actual_size = 0
        new_population = [indv for indv in self.best_indviduals]
        print(f"New population with best: {new_population}")
        while actual_size < size:
            self.get_parents()
            children = self.crossover()
            if actual_size + len(children) > size:
                child_number = random.randint(1, len(children))
                children = children[:child_number]
            for child in children:
                new_population.append(child)
                actual_size += 1
                print(f"Child: {child}")

        return new_population
    

class SinglePointCrossover(Crossover):
    def crossover(self) -> list[Individual]:
        point = random.randint(1, self.parent1.length - 1)
        child1_chromosomes = self.parent1.chromosomes[:point] + self.parent2.chromosomes[point:]
        child2_chromosomes = self.parent2.chromosomes[:point] + self.parent1.chromosomes[point:]
        child1 = Individual(parent = self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent = self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]
    
class TwoPointCrossover(Crossover):
    def crossover(self) -> list[Individual]:
        point1 = random.randint(1, self.parent1.length - 2)
        point2 = random.randint(point1 + 1, self.parent1.length - 1)
        child1_chromosomes = self.parent1.chromosomes[:point1] + self.parent2.chromosomes[point1:point2] + self.parent1.chromosomes[point2:]
        child2_chromosomes = self.parent2.chromosomes[:point1] + self.parent1.chromosomes[point1:point2] + self.parent2.chromosomes[point2:]
        child1 = Individual(parent = self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent = self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]
    
class UniformCrossover(Crossover):
    def __init__(self, population: list[Individual], best_indviduals: list[Individual], whole_pop_size: int, probability: float = 0.7) -> None:
        super().__init__(population, best_indviduals, whole_pop_size)
        self.probability = probability
        if self.probability < 0 or self.probability > 1:
            raise ValueError("Probability must be between 0 and 1")
        
    def crossover(self) -> list[Individual]:
        child1_chromosomes = []
        child2_chromosomes = []
        for i in range(self.parent1.n):
            if random.random() < self.probability:
                child1_chromosomes.append(self.parent1.chromosomes[i])
                child2_chromosomes.append(self.parent2.chromosomes[i])
            else:
                child1_chromosomes.append(self.parent2.chromosomes[i])
                child2_chromosomes.append(self.parent1.chromosomes[i])
        child1 = Individual(parent = self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent = self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]
    

class DiscreteCrossover(Crossover):
    def __init__(self, population: list[Individual], best_indviduals: list[Individual], whole_pop_size: int, probability: float = 0.5) -> None:
        super().__init__(population, best_indviduals, whole_pop_size)
        self.probability = probability
        if self.probability < 0 or self.probability > 1:
            raise ValueError("Probability must be between 0 and 1")
        
    def crossover(self) -> list[Individual]:
        child_chromosomes = []
        for i in range(self.parent1.n):
            if random.random() < self.probability:
                child_chromosomes.append(self.parent1.chromosomes[i])
            else:
                child_chromosomes.append(self.parent2.chromosomes[i])
        child = Individual(parent = self.parent1, chromosomes=child_chromosomes)
        return [child]   
