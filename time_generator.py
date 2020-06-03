""" Random time generators to be used for inter arrival time or activity time in simulation models.
"""

import random
from math import sqrt, log


class TimeGenerator:
    class Uniform(random.Random):
        def __init__(self, lower_limit=0, upper_limit=1, **kwargs):
            self.x = None
            self.lower_limit = lower_limit
            self.upper_limit = upper_limit
            for key, value in kwargs.items():
                if key == "seed":
                    setattr(self, "x", value)
            super().__init__(self.x)

        def generate(self):
            return round(self.random() * (self.upper_limit - self.lower_limit) + self.lower_limit, 3)

    class Exponential(random.Random):
        def __init__(self, mean=1, **kwargs):
            self.x = None
            self.rate = 1 / mean
            for key, value in kwargs.items():
                if key == "seed":
                    setattr(self, "x", value)
            super().__init__(self.x)

        def generate(self):
            rnd = self.random()
            return round(-1 / self.rate * log(rnd), 3)

    class Triangular(random.Random):
        def __init__(self, lower_limit=0, mode=.5, upper_limit=1, **kwargs):
            self.x = None
            self.a = lower_limit
            self.b = upper_limit
            self.c = mode
            self.Fc = (self.c - self.a) / (self.b - self.a)
            for key, value in kwargs.items():
                if key == "seed":
                    setattr(self, "x", value)
            super().__init__(self.x)

        def generate(self):
            rnd = self.random()
            if rnd < self.Fc:
                return round(self.a + sqrt(rnd * (self.b - self.a) * (self.c - self.a)), 3)
            return round(self.b - sqrt((1 - rnd) * (self.b - self.a) * (self.b - self.c)), 3)

    class DoubleTriangular(random.Random):
        def __init__(self, lower_limit_1=0, mode_1=0.5, upper_limit_1=1, lower_limit_2=0, mode_2=.5, upper_limit_2=1, **kwargs):
            self.x = None
            self.a1 = lower_limit_1
            self.b1 = upper_limit_1
            self.c1 = mode_1
            self.a2 = lower_limit_2
            self.b2 = upper_limit_2
            self.c2 = mode_2
            self.Fc1 = (self.c1 - self.a1) / (self.b1 - self.a1)
            self.Fc2 = (self.c2 - self.a2) / (self.b2 - self.a2)
            for key, value in kwargs.items():
                if key == "seed":
                    setattr(self, "x", value)
            super().__init__(self.x)

        def generate(self):
            rnd1 = self.random()
            rnd2 = self.random()

            if rnd1 < self.Fc1:
                t1 = round(self.a1 + sqrt(rnd1 * (self.b1 - self.a1) * (self.c1 - self.a1)), 3)
            else:
                t1 = round(self.b1 - sqrt((1 - rnd1) * (self.b1 - self.a1) * (self.b1 - self.c1)), 3)

            if rnd2 < self.Fc2:
                t2 = round(self.a2 + sqrt(rnd2 * (self.b2 - self.a2) * (self.c2 - self.a2)), 3)
            else:
                t2 = round(self.b2 - sqrt((1 - rnd2) * (self.b2 - self.a2) * (self.b2 - self.c2)), 3)

            return t1 + t2

    class DT:
        def __init__(self, triangular_obj_1, triangular_obj_2):
            self.t1 = triangular_obj_1
            self.t2 = triangular_obj_2

        def generate(self):
            return self.t1.generate() + self.t2.generate()
