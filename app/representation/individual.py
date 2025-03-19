from chromosome import Chromosome

class Individual:
    def __init__(self, a: int, b:int , function, length: int, n: int) -> None:
        '''
        todo, for now n - number of func variables
        '''
        self.a = a
        self.b = b
        self.function = function
        self.length = length
        self.n = n
        self.chromosomes = [Chromosome(length) for _ in range(n)]


    def decode(self) -> int:
        all_values = []
        for chromosome in self.chromosomes:
            binary_chain = chromosome.get_binary_chain()
            decimal_repr = int(binary_chain, 2)
            val = self.a + decimal_repr * (self.b - self.a)/(2**self.length-1)
            all_values.append(val)
        return all_values
    
    def target_function(self, x_values : list):
       
        target_val = self.function(*x_values)
        return target_val

    def __str__(self):
        return f"Individual with {self.n} chromosomes: {self.chromosomes}"
    

    def __repr__(self):
        return f"Individual with {self.n} chromosomes: {self.chromosomes}"


