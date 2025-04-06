from typing import Callable, Tuple, Optional
import numpy as np


class FunctionWrapper:
    def __init__(
        self,
        constructor: Optional[Callable] = None,
        bounds: Tuple[float, float] = (-10, 10),
        dimensions: Tuple[int] = None,
        is_exactly_2d: bool = False,
    ):
        self.constructor = constructor
        self.__name__ = constructor.__name__
        self.bounds = bounds
        self.dimensions = dimensions
        self.is_exactly_2d = is_exactly_2d

    def __call__(self, n_dimensions=2):
        if self.is_exactly_2d and n_dimensions != 2:
            raise ValueError(f"Funkcja {self.__name__} obsługuje tylko 2 wymiary.")
        if self.dimensions and n_dimensions not in self.dimensions:
            raise ValueError(
                f"Funkcja {self.__name__} obsługuje {self.dimensions} wymiarów."
            )
        if self.dimensions:  # wtedy funkcja jest z opfunu

            class FuncInstance:
                def __init__(self, method):
                    self.method = method

                def __call__(self, x: np.ndarray):
                    return self.method.evaluate(x)

            return FuncInstance(self.constructor(ndim=n_dimensions))
        elif self.constructor:
            instance = (
                self.constructor(n_dimensions=n_dimensions)
                if not self.is_exactly_2d
                else self.constructor()
            )

            return instance
        else:
            raise ValueError("Nie podano implementacji funkcji.")

    def get_bounds(self):
        return self.bounds
