from app.representation.chromosome import Chromosome
from typing import List
import random


class Individual:
    def __init__(
        self,
        a: int = None,
        b: int = None,
        function=None,
        length: int = None,
        n: int = None,
        precission: int = None,
        chromosomes: List[int] = None,
        parent=None,
        real_representation: bool = False,
        real_values: List[float] = None,
    ):
        """
        Initialize an Individual either directly or from a parent.
        """
        if parent:
            # Initialize from parent with real representation
            self.a = parent.a
            self.b = parent.b
            self.function = parent.function
            self.length = parent.length
            self.n = parent.n
            self.precission = parent.precission
            if real_representation:
                self.real_values = real_values
            else:
                self.chromosomes = chromosomes
                self.decodes = self.decode()
        else:
            # Initialize directly
            self.a = a
            self.b = b
            self.function = function
            self.length = length
            self.n = n
            self.precission = precission
            if real_representation:
                self.real_values = [random.uniform(a, b) for _ in range(n)]
            else:
                self.chromosomes = [Chromosome(length) for _ in range(n)]
                self.decodes = self.decode()


        self.target_function_val = self.target_function(self.real_values if real_representation else self.decodes) 

    def decode(self) -> int:
        all_values = []
        for chromosome in self.chromosomes:
            binary_chain = chromosome.get_binary_chain()
            decimal_repr = int(binary_chain, 2)
            val = self.a + decimal_repr * (self.b - self.a) / (2**self.length - 1)
            all_values.append(val)
        return all_values

    def target_function(self, x_values: list):
        target_val = self.function(x_values)
        if self.precission:
            target_val = round(target_val, self.precission)
        return target_val

    def __str__(self):
        if self.real_values:
            return f"Individual with {self.n} real values: {self.real_values} target func: {self.target_function_val}"
        return f"Individual with {self.n} chromosomes: {self.chromosomes} target func: {self.target_function_val}"

    def __repr__(self):
        if self.real_values:
            return f"Individual with {self.n} real values: {self.real_values} target func: {self.target_function_val}"
        return f"Individual with {self.n} chromosomes: {self.chromosomes} target func: {self.target_function_val}"
