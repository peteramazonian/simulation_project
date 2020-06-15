import time_management
from time_management import add_to_fel

__id__ = 10000

# TODO new arrivals in fel dont have id?!?


def id_generator():
    global __id__
    __id__ += 1
    return __id__


class SystemArrival:
    list = []
    costumers_inside_dict = {}
    costumers_departured = 0
    costumers_total_time = 0
    result = {}

    @classmethod
    def departure(cls, costumer_id):
        cls.costumers_departured += 1
        cls.costumers_total_time += time_management.clock - cls.costumers_inside_dict[costumer_id]
        cls.costumers_inside_dict.pop(costumer_id)

    def __init__(self, name, inter_arrival_time_generator, number_of_arrivals_generator):
        self.name = name
        self.time_generator = inter_arrival_time_generator
        self.number_generator = number_of_arrivals_generator
        SystemArrival.list.append(self)
        self.m_list = __import__('movement').Movement.list

    # Overriding Python's original __repr__ function
    def __repr__(self):
        return self.name

    def set_first_arrival(self, beginning_time):
        event_notice = (
            self.time_generator.generate() + beginning_time, self.name, self.number_generator.generate(),
            self.new_arrival)
        add_to_fel(event_notice)

    def new_arrival(self, number_of_arrivals):
        for i in range(number_of_arrivals):
            id_tmp = id_generator()
            SystemArrival.costumers_inside_dict[id_tmp] = time_management.clock
            self.m_list[0].move(id_tmp)
        # generating next arrival event
        event_notice = (
            self.time_generator.generate() + time_management.clock, self.name, self.number_generator.generate(),
            self.new_arrival)
        add_to_fel(event_notice)

    def set_single_arrival(self, beginning_time):
        event_notice = (
            self.time_generator.generate() + beginning_time, self.name, self.number_generator.generate(),
            self.new_single_arrival)
        add_to_fel(event_notice)

    def new_single_arrival(self, number_of_arrivals):
        for i in range(number_of_arrivals):
            id_tmp = id_generator()
            SystemArrival.costumers_inside_dict[id_tmp] = time_management.clock
            self.m_list[0].move(id_tmp)

    @classmethod
    def final_calculations(cls):
        cls.result = dict(average_time_in_system=cls.costumers_total_time / cls.costumers_departured)
