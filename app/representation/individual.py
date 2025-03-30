from app.representation.chromosome import Chromosome
from typing import List

class Individual:
    def __init__(self, a: int = None, b: int = None, function=None, length: int = None, n: int = None, precission:int = None, chromosomes: List[int] = None, parent=None):
        '''
        Initialize an Individual either directly or from a parent.
        '''
        if parent:
            # Initialize from parent
            self.a = parent.a
            self.b = parent.b
            self.function = parent.function
            self.length = parent.length
            self.n = parent.n
            self.chromosomes = chromosomes
            self.precission = parent.precission
        else:
            # Initialize directly
            self.a = a
            self.b = b
            self.function = function
            self.length = length
            self.n = n
            self.precission = precission
            self.chromosomes = [Chromosome(length) for _ in range(n)]
        
        self.decodes = self.decode()
        self.target_function_val = self.target_function(self.decodes)

    def decode(self) -> int:
        all_values = []
        for chromosome in self.chromosomes:
            binary_chain = chromosome.get_binary_chain()
            decimal_repr = int(binary_chain, 2)
            val = self.a + decimal_repr * (self.b - self.a) / (2**self.length - 1)
            all_values.append(val)
        return all_values

    def target_function(self, x_values: list):
        target_val = self.function(*x_values)
        print(f"PRECISSION {self.precission}")
        if self.precission:
            target_val = round(target_val, self.precission)
            print(f"Target value with precision {self.precission}: {target_val}")
        return target_val

    def __str__(self):
        return f"Individual with {self.n} chromosomes: {self.chromosomes} target func: {self.target_function_val}"

    def __repr__(self):
        return f"Individual with {self.n} chromosomes: {self.chromosomes} target func: {self.target_function_val}"