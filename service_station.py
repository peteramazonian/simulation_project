class ServiceStation():
    def __init__(self, name, service_time, a, b):
        self.a = a
        self.b = b
        self.service_time = service_time
        self.name = name
    def arrival(self, time):
        x = self.service_time(self.a ,self.b)
        print ("new arrival for %s at %s" %(self.name, time))
        print ("service time at %s is %s" %(self.name, x))
        print ("departure from %s at %s" %(self.name, time + x))
        self.departure(time + x)
    def departure(self, time):
        print ("------------just departured from %s at %s" %(self.name, time))
