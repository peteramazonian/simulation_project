from time_generator import TimeGenerator
class ServiceStation():
    def __init__(self, name, service_time_generator: TimeGenerator, servers):
        self.name = name
        self.service_time_generator = service_time_generator
        #self.service_time_generator is an object made of TimeGenerator class
        self.servers = servers

    def arrival(self, time):
        x = self.service_time_generator.generate()
        print("new arrival for %s   at   %s" % (self.name, time))
        print("service time at %s   is   %s" % (self.name, x))
        print("departure from  %s   at   %s" % (self.name, time + x))
        self.departure(time + x)

    def departure(self, time):
        print("-----------------------------just departured from %s   at    %s" % (self.name, time))
