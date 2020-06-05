import time_management
from time_management import add_to_fel
from system_arrival import SystemArrival
ss_list = __import__('service_station').ServiceStation.list


class Movement():
    list = []
    @classmethod
    def check(cls):
        x = len(ss_list)
        if len(cls.list) == x + 1:
            return
        elif len(cls.list) < x + 1:
            raise ValueError("Movement objects should be more")
        else:
            raise ValueError("Movement objects are more than needed")

    def __init__(self, moving_time_generator):
        self.time_generator = moving_time_generator
        self.position = len(Movement.list) + 1
        self.name = "m" + str(self.position)
        Movement.list.append(self)

    # Overriding Python's original __repr__ function
    def __repr__(self):
        return self.name

    def move(self, costumer_id):
        if self.position <= len(ss_list):
            event_notice = (
                self.time_generator.generate() + time_management.clock, "A" + str(self.position), costumer_id,
                ss_list[self.position - 1].arrival)
            add_to_fel(event_notice)
        else:
            event_notice = (self.time_generator.generate() + time_management.clock, "D", costumer_id, SystemArrival.departure)
            add_to_fel(event_notice)

