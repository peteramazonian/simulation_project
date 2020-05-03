""" Random time generators to be used for inter arrival time or activity time in simulation models.
"""

import random


class TimeGenerator():
    class Uniform(random.Random):
        def __init__(self, lower_limit=0, upper_limit=1):
            self.lower_limit = lower_limit
            self.upper_limit = upper_limit

        def generate(self):
            return self.random() * (self.upper_limit - self.lower_limit) + self.lower_limit

        def seed_set(self, seed):
            self.seed(seed)
            self.seed = seed
'''
    class Triangular(self, lower_limit=0, mean=.5, upper_limit=1):
        pass
'''