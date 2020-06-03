import time_management
from time_management import add_to_fel

__id__ = 10000


def id_generator():
    global __id__
    __id__ += 1
    return __id__


class SystemArrival:
    list = []

    def __init__(self, name, inter_arrival_time_generator, number_of_arrivals_generator):
        self.name = name
        self.time_generator = inter_arrival_time_generator
        self.number_generator = number_of_arrivals_generator
        SystemArrival.list.append(self)
        self.m_list = __import__('movement').Movement.list

    # Overriding Python's original __repr__ function
    def __repr__(self):
        return self.name

    def new_arrival(self, number_of_arrivals):
        for i in range(number_of_arrivals):
            self.m_list[0].move(id_generator())
        # generating next arrival event
        event_notice = (
            self.time_generator.generate() + time_management.clock, self.name, self.number_generator.generate(), self.new_arrival)
        add_to_fel(event_notice)


def departure(costumer_id):
    print("%s   Departured at   %s" % (costumer_id, time_management.clock))
