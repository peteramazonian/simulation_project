from time_generator import TimeGenerator
from time_management import add_to_fel, clock
import random

__id__ = 10000


def id_generator():
    global __id__
    __id__ += 1
    return __id__


class NumberGenerator():
    # TODO define number generator
    class Static(random.Random):
        pass

    class Poisson(random.Random):
        pass

    class Discrete(random.Random):
        def __init__(self, x: tuple, fx: tuple, *args):
            self.fx_list = fx
            self.x_list = x
            if len(self.x_list) != len(self.fx_list):
                raise ValueError("x_list and fx_list should have same number of elements")
            super().__init__(*args)

        def generate(self):
            rnd = self.random()
            print (rnd)
            for i in range(self.fx_list.__len__()):
                if rnd < sum(self.fx_list[:i + 1]):
                    return self.x_list[i]



class SystemArrival:
    def __init__(self, name, inter_arrival_time_generator, number_of_arrivals_generator):
        self.name = name
        self.time_generator = inter_arrival_time_generator
        self.number_generator = number_of_arrivals_generator

    # Overriding Python's original __repr__ function
    def __repr__(self):
        return self.name

    def new_arrival(self, number_of_arrivals):
        for i in range(number_of_arrivals):
            # TODO define movement
            movement[0](id_generator())
        # generating next arrival event
        event_notice = (self.time_generator.generate() + clock, self.name, self.number_generator.generate(), self.new_arrival)
        add_to_fel(event_notice)
