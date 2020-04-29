""" Random time generators to be used for inter arrival time or activity time in simulation models.
"""

import random

class TimeGenerator():
    def __init__(self,seed):
        random.seed(seed)

    def uniform (self, lower_limit = 0 , upper_limit = 1):
        return random.random()*(upper_limit-lower_limit)+lower_limit

    def triangular(self, lower_limit = 0 , mean = .5 , upper_limit = 1):
        pass

