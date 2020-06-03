import time_management
from time_management import add_to_fel, postponed_rest_log_editor


# ----------------------------------------------------------------
# Creating class ServiceStation
# Our service stations are objects of this class
# Costumer arrivals, departures, servers leaving for rest and getting back to work are handled here
# ----------------------------------------------------------------
# event notices created here are as follow:
# station departure:        (time, Di, costumer_id, method)
# server rest:              (time, Ri, method)
# server back:              (time, Bi, method)

class ServiceStation:
    list = []

    def __init__(self, name, service_time_generator, available_servers):
        self.name = name  # What you call this station in real world
        self.service_time_generator = service_time_generator  # Service_time_generator is an object of TimeGenerator cls
        self.available_servers = available_servers  # Number of servers working in this ServiceStation
        self.busy_servers = 0  # Number of busy servers at the beginning of the simulation. Usually equals to 0
        self.queue_list = []  # List of costumers waiting in queue for this station. queue_list elements:
        # (queue_joined_time, costumer_id)
        self.rest_in_waiting = 0  # When there is a server waiting to finish the serve, then go to rest, this will be
        # equal to 1
        self.server_rest_duration = 10  # How long is each server's rest duration
        self.position = len(ServiceStation.list) + 1
        ServiceStation.list.append(self)
        self.m_list = __import__('movement').Movement.list
        # --------------------------------------------------------
        # Variables to measure system evaluation parameters:
        self.cumulative_q_len = 0
        self.q_len_last_clock = 0

    # Overriding Python's original __repr__ function
    def __repr__(self):
        return self.name

    # Handles arrivals to this station.
    def arrival(self, costumer_id):
        if self.busy_servers < self.available_servers:  # No waiting in Queue
            self.busy_servers += 1
            event_notice = (
                self.service_time_generator.generate() + time_management.clock, "D" + str(self.position), costumer_id, self.departure)
            add_to_fel(event_notice)  # Generating departure event for this costumer.
        else:  # Waiting in queue
            print("clock = %s" % time_management.clock)
            self.cumulative_q_len += len(self.queue_list) * (time_management.clock - self.q_len_last_clock)
            self.q_len_last_clock = time_management.clock
            self.queue_list.append((time_management.clock, costumer_id))  # Adding costumer to queue

    # Handles all departures from this station. departure will happen when service ends for one costumer.
    def departure(self, costumer_id):
        if not self.rest_in_waiting:  # If there is no server waiting to get rest.
            if self.queue_list.__len__() > 0:
                event_notice = (
                    self.service_time_generator.generate() + time_management.clock, "D" + str(self.position), self.queue_list[0][1],
                    self.departure)
                add_to_fel(event_notice)  # Generating departure event for next costumer waiting in queue.
                del self.queue_list[0]  # Deleting the costumer which starts getting service, from queue.
            else:
                self.busy_servers -= 1
        else:  # If there is a server waiting to get rest
            self.busy_servers -= 1  # The server is no longer busy
            self.rest_in_waiting = 0  # so there is no busy server, waiting to get rest
            event_notice = (time_management.clock, "R" + str(self.position), self.server_rest)
            add_to_fel(event_notice)  # Generating the new server rest event notice
            # Adding this new event notice to fel is necessary for fel logging
        self.m_list[self.position].move(costumer_id)

    # Handles server rest periods. in this model, server rest event notices are initialized in fel.
    def server_rest(self, *args):
        if self.busy_servers < self.available_servers:
            self.available_servers -= 1
            event_notice = (self.server_rest_duration + time_management.clock, "B" + str(self.position), self.server_back)
            add_to_fel(event_notice)  # Generates event notice for server coming back from rest after 10 mins.
        else:
            self.rest_in_waiting = 1  # It's used in departure() method.
            postponed_rest_log_editor()

    # Handles when a server is back from rest and starts serving a new costumer if queue is not empty.
    def server_back(self, *args):
        self.available_servers += 1
        if self.queue_list.__len__() > 0:
            event_notice = (
                self.service_time_generator.generate() + time_management.clock, "D" + str(self.position), self.queue_list[0][1],
                self.departure)
            add_to_fel(event_notice)  # Generating departure event for next costumer waiting in queue.
            del self.queue_list[0]  # Deleting the costumer which starts getting service, from queue.
