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

    def __init__(self, name, service_time_generator, num_of_servers):
        self.name = name  # What you call this station in real world
        self.service_time_generator = service_time_generator  # Service_time_generator is an object of TimeGenerator cls
        self.num_of_servers = num_of_servers    # Number of servers working in this ServiceStation
        self.available_servers = num_of_servers
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
        self.q_len_cumulative = 0
        self.q_len_last_clock = 0
        self.q_len_max = 0
        # ---
        self.service_total_time = 0
        self.service_total_count = 0
        # ---
        self.servers_total_busy_t = 0   # Sum of busy servers * time in different periods
        self.servers_busy_last_clock = 0    # Last time the busy servers number changed
        self.servers_total_available_t = 0  # Sum of available servers * time in different periods
        self.servers_available_last_clock = 0   # Last time the available servers number changed

    # Overriding Python's original __repr__ function
    def __repr__(self):
        return self.name

    def return_printables(self):
        return([self.available_servers, self.busy_servers, len(self.queue_list), self.rest_in_waiting,
                           self.q_len_cumulative, self.q_len_max, self.service_total_time, self.service_total_count,
                           self.servers_total_busy_t, self.servers_total_available_t])

    # Handles arrivals to this station.
    def arrival(self, costumer_id):
        if self.busy_servers < self.available_servers:  # No waiting in Queue
            self.servers_total_busy_t += self.busy_servers * (time_management.clock - self.servers_busy_last_clock)
            self.servers_busy_last_clock = time_management.clock
            self.busy_servers += 1
            event_duration = self.service_time_generator.generate()
            event_notice = (
                event_duration + time_management.clock, "D" + str(self.position), costumer_id, self.departure)
            add_to_fel(event_notice)  # Generating departure event for this costumer.
            self.service_total_time += event_duration
            self.service_total_count += 1
        else:  # Waiting in queue
            self.q_len_cumulative += len(self.queue_list) * (time_management.clock - self.q_len_last_clock)
            self.q_len_last_clock = time_management.clock
            self.queue_list.append((time_management.clock, costumer_id))  # Adding costumer to queue
            if len(self.queue_list) > self.q_len_max:
                self.q_len_max = len(self.queue_list)

    # Handles all departures from this station. departure will happen when service ends for one costumer.
    def departure(self, costumer_id):
        if not self.rest_in_waiting:  # If there is no server waiting to get rest.
            if self.queue_list.__len__() > 0:
                event_duration = self.service_time_generator.generate()
                event_notice = (
                    event_duration + time_management.clock, "D" + str(self.position), self.queue_list[0][1],
                    self.departure)
                add_to_fel(event_notice)  # Generating departure event for next costumer waiting in queue.
                self.service_total_time += event_duration
                self.service_total_count += 1
                self.q_len_cumulative += len(self.queue_list) * (time_management.clock - self.q_len_last_clock)
                self.q_len_last_clock = time_management.clock
                del self.queue_list[0]  # Deleting the costumer which starts getting service, from queue.
            else:
                self.servers_total_busy_t += self.busy_servers * (time_management.clock - self.servers_busy_last_clock)
                self.servers_busy_last_clock = time_management.clock
                self.busy_servers -= 1
        else:  # If there is a server waiting to get rest
            self.servers_total_busy_t += self.busy_servers * (time_management.clock - self.servers_busy_last_clock)
            self.servers_busy_last_clock = time_management.clock
            self.busy_servers -= 1  # The server is no longer busy
            self.rest_in_waiting = 0  # so there is no busy server, waiting to get rest
            event_notice = (time_management.clock, "R" + str(self.position), self.server_rest)
            add_to_fel(event_notice)  # Generating the new server rest event notice
            # Adding this new event notice to fel is necessary for fel logging
        self.m_list[self.position].move(costumer_id)

    # Handles server rest periods. in this model, server rest event notices are initialized in fel.
    def server_rest(self, *args):
        if self.busy_servers < self.available_servers:
            self.servers_total_available_t += self.available_servers * (time_management.clock - self.servers_available_last_clock)
            self.servers_available_last_clock = time_management.clock
            self.available_servers -= 1
            event_notice = (self.server_rest_duration + time_management.clock, "B" + str(self.position), self.server_back)
            add_to_fel(event_notice)  # Generates event notice for server coming back from rest after 10 mins.
        else:
            self.rest_in_waiting = 1  # It's used in departure() method.
            postponed_rest_log_editor()

    # Handles when a server is back from rest and starts serving a new costumer if queue is not empty.
    def server_back(self, *args):
        self.servers_total_available_t += self.available_servers * (time_management.clock - self.servers_available_last_clock)
        self.servers_available_last_clock = time_management.clock
        self.available_servers += 1
        if self.queue_list.__len__() > 0:
            self.servers_total_busy_t += self.busy_servers * (time_management.clock - self.servers_busy_last_clock)
            self.servers_busy_last_clock = time_management.clock
            self.busy_servers += 1
            event_duration = self.service_time_generator.generate()
            event_notice = (
                event_duration + time_management.clock, "D" + str(self.position), self.queue_list[0][1],
                self.departure)
            add_to_fel(event_notice)  # Generating departure event for next costumer waiting in queue.
            self.service_total_time += event_duration
            self.service_total_count += 1
            self.q_len_cumulative += len(self.queue_list) * (time_management.clock - self.q_len_last_clock)
            self.q_len_last_clock = time_management.clock
            del self.queue_list[0]  # Deleting the costumer which starts getting service, from queue.

    def set_rest_times(self, rest_times_list):
        for t in rest_times_list:
            event_notice = (t, "R" + str(self.position), self.server_rest)
            add_to_fel(event_notice)
