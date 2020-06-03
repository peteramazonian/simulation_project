import random
from math import exp


class NumberGenerator:
    class Discrete(random.Random):
        def __init__(self, x: tuple, fx: tuple, **kwargs):
            self.x = None
            self.fx_list = fx
            self.x_list = x
            if len(self.x_list) != len(self.fx_list):
                raise ValueError("x_list and fx_list should have same number of elements")
            for key, value in kwargs.items():
                if key == "seed":
                    setattr(self, "x", value)
            super().__init__(self.x)

        def generate(self):
            rnd = self.random()
            for i in range(self.fx_list.__len__()):
                if rnd < sum(self.fx_list[:i + 1]):
                    return self.x_list[i]

    class Static:
        def __init__(self, x=0):
            self.x = x

        def generate(self):
            return self.x

    class Poisson(random.Random):
        def __init__(self, mean=1, **kwargs):
            self.x = None
            self.mean = mean
            self.e = exp(-1 * mean)
            for key, value in kwargs.items():
                if key == "seed":
                    setattr(self, "x", value)
            super().__init__(self.x)

        def generate(self):
            n = -1
            p = 1
            while p > self.e:
                p = p * self.random()
                n += 1
            return n
