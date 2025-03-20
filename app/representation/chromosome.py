from random import randint

class Chromosome:
    def __init__(self, length:int):
        self.length = length
        self._generate_gens()

    def _generate_gens(self):
        self.gens = [randint(0,1) for _ in range(self.length)]

    def get_binary_chain(self):
        return "".join(str(ele) for ele in self.gens)

    def __str__(self):
        return f"Chromosome with gens: {self.gens}"
    
    def __repr__(self):
        return f"{self.gens}"
    
