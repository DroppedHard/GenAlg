import random
from app.representation.individual import Individual
from app.representation.population import Population

class Crossover:
    def __init__(self, population: Population) -> None:
        self.population: Population = population

    def get_parents(self) -> None:
        self.parent1 = random.choice(self.population.population)
        self.parent2 = random.choice(self.population.population)
        while self.parent1 == self.parent2:
            self.parent2 = random.choice(self.population.population)

    def crossover(self):
        raise NotImplementedError("Crossover method not implemented.")
    
    def crossover_population(self) -> list[Individual]:
        size = self.population.population_size - self.population.best_indv_number
        actual_size = 0
        new_population = [indv for indv in self.population.get_best_individuals()]
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
    def crossover(self) -> list[Individual]:
        child1_chromosomes = []
        child2_chromosomes = []
        for i in range(self.parent1.n):
            if random.random() < 0.7:
                child1_chromosomes.append(self.parent1.chromosomes[i])
                child2_chromosomes.append(self.parent2.chromosomes[i])
            else:
                child1_chromosomes.append(self.parent2.chromosomes[i])
                child2_chromosomes.append(self.parent1.chromosomes[i])
        child1 = Individual(parent = self.parent1, chromosomes=child1_chromosomes)
        child2 = Individual(parent = self.parent2, chromosomes=child2_chromosomes)
        return [child1, child2]
    

class DiscreteCrossover(Crossover):
    def crossover(self) -> list[Individual]:
        child_chromosomes = []
        for i in range(self.parent1.n):
            if random.random() < 0.5:
                child_chromosomes.append(self.parent1.chromosomes[i])
            else:
                child_chromosomes.append(self.parent2.chromosomes[i])
        child = Individual(parent = self.parent1, chromosomes=child_chromosomes)
        return [child]   
