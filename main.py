from service_station import ServiceStation
from system_arrival import SystemArrival
from movement import Movement
from time_generator import TimeGenerator
from number_generator import NumberGenerator
import time_management
from logger import Logger

# Its our simulation's main file.
# Here we import classes and functions from other project files.
# Then we need to make objects from our classes and set attributes.
# These objects are used to setup the system in a modular way.
# You can make as many service stations as you need with their own attributes, then arrange the whole system together.

# ---------------------------------------------------------------------
#                   Creating SystemArrival objects
# ---------------------------------------------------------------------

# -------- First SystemArrival object --------
t_generator = TimeGenerator.Uniform(1, 1, seed=1212)  # Creating its TimeGenerator
n_generator = NumberGenerator.Discrete((1, 1, 1), (0.2, 0.3, 0.5), seed=1010)  # Creating its NumberGenerator
ief = SystemArrival("ief", t_generator, n_generator)  # Creating first SystemArrival object
del n_generator, t_generator

# ---------------------------------------------------------------------
#                   Creating ServiceStation objects
# ---------------------------------------------------------------------

# -------- First ServiceStation object --------
t_generator = TimeGenerator.Uniform(10, 10, seed=1020)  # Creating its TimeGenerator
ss1 = ServiceStation("ss1", t_generator, 5)  # Creating first ServiceStation object
del t_generator

# -------- Second ServiceStation object --------
t_generator = TimeGenerator.Uniform(2, 2, seed=4040)  # Creating its TimeGenerator
ss2 = ServiceStation("ss2", t_generator, 2)  # Creating first ServiceStation object
del t_generator

# -------- Third ServiceStation object --------
t_generator = TimeGenerator.Uniform(2, 2, seed=3030)  # Creating its TimeGenerator
ss3 = ServiceStation("ss3", t_generator, 30)  # Creating first ServiceStation object
del t_generator

# ---------------------------------------------------------------------
#                   Creating Movement objects
# ---------------------------------------------------------------------

m1 = Movement(TimeGenerator.Uniform(1, 1, seed=8080))
m2 = Movement(TimeGenerator.Uniform(1, 1, seed=8080))
m3 = Movement(TimeGenerator.Uniform(1, 1, seed=8080))
m4 = Movement(TimeGenerator.Uniform(1, 1, seed=8080))

Movement.check()




# Setting the simulation's duration
ief.new_arrival(0)
time_management.add_to_fel((60, "R1", ss1.server_rest))
time_management.add_to_fel((120, "R1", ss1.server_rest))
time_management.add_to_fel((180, "R1", ss1.server_rest))
time_management.add_to_fel((240, "R1", ss1.server_rest))
i = 0
while i < 1000:
    # x = input("'y' to continue,   'e' to exit")
    # if x == 'y':
    time_management.advance_time()
    i += 1
    print(i)
    # elif x == 'e':
    #     break

time_management.close_logger()