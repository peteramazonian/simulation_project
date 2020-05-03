from time_generator import TimeGenerator
from time_management import add_to_fel
class ServiceStation():
    def __init__(self, name, service_time_generator: TimeGenerator, available_servers):
        self.name = name
        self.service_time_generator = service_time_generator
        '''self.service_time_generator is an object made of TimeGenerator class'''
        self.AS = available_servers
        self.BS = 0
        self.Q = 0

    def arrival(self):
        if(self.BS < self.AS):
            self.BS += 1
            event_notice = (time + self.service_time_generator.generate(), self.departure)
            add_to_fel(event_notice)
        else:
            self.Q += 1

    def departure(self, time):
        if(self.Q > 0):
            self.Q -= 1
        else:
            self.BS -= 1
