from individual import Individual


class Population:
    def __init__(self, a, b, func, n_of_variables, chrom_length, population_size, epochs):
        self.a = a
        self.b = b
        self.func = func
        self.n_of_variables = n_of_variables
        self.chrom_length = chrom_length
        self.population_size = population_size
        self.epochs = epochs
        self.population = self.create_population()


    def create_population(self):
        return [Individual(self.a, self.b, self.func, self.chrom_length, self.n_of_variables) for _ in range(self.population_size)]

