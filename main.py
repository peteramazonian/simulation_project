from service_station import ServiceStation
from system_arrival import SystemArrival
from movement import Movement
from time_generator import TimeGenerator
from number_generator import NumberGenerator
import time_management

# Its our simulation's main file.
# Here we import classes and functions from other project files.
# Then we need to make objects from our classes and set attributes.
# These objects are used to setup the system in a modular way.
# You can make as many service stations as you need with their own attributes, then arrange the whole system together.

# ---------------------------------------------------------------------
#                   Creating SystemArrival objects
# ---------------------------------------------------------------------

# -------- First SystemArrival object --------
t_generator = TimeGenerator.Exponential(3)  # Creating its TimeGenerator
n_generator = NumberGenerator.Static(1)  # Creating its NumberGenerator
ief1 = SystemArrival("ief1", t_generator, n_generator)  # Creating first SystemArrival object
del n_generator, t_generator

# -------- Second SystemArrival object --------
t_generator = TimeGenerator.Exponential(5)  # Creating its TimeGenerator
n_generator = NumberGenerator.Discrete((1, 2, 3, 4), (0.2, 0.3, 0.3, 0.2))  # Creating its NumberGenerator
ief2 = SystemArrival("ief2", t_generator, n_generator)  # Creating first SystemArrival object
del n_generator, t_generator

# -------- Third SystemArrival object --------
t_generator = TimeGenerator.Uniform(0, 120)  # Creating its TimeGenerator
n_generator = NumberGenerator.Poisson(30)  # Creating its NumberGenerator
ief3 = SystemArrival("ief3", t_generator, n_generator)  # Creating first SystemArrival object
del n_generator, t_generator

# ---------------------------------------------------------------------
#                   Creating ServiceStation objects
# ---------------------------------------------------------------------

# -------- First ServiceStation object --------
t_generator = TimeGenerator.DoubleTriangular(1, 2, 4, 1, 2, 3)  # Creating its TimeGenerator
ss1 = ServiceStation("ss1", t_generator, 5)  # Creating first ServiceStation object
del t_generator

# -------- Second ServiceStation object --------
t_generator = TimeGenerator.Uniform(0.5, 2)  # Creating its TimeGenerator
ss2 = ServiceStation("ss2", t_generator, 2)  # Creating first ServiceStation object
del t_generator

# -------- Third ServiceStation object --------
t_generator = TimeGenerator.Triangular(10, 20, 30)  # Creating its TimeGenerator
ss3 = ServiceStation("ss3", t_generator, 30)  # Creating first ServiceStation object
del t_generator

# ---------------------------------------------------------------------
#                   Creating Movement objects
# ---------------------------------------------------------------------

m1 = Movement(TimeGenerator.Static(0))
m2 = Movement(TimeGenerator.Exponential(0.5))
m3 = Movement(TimeGenerator.Exponential(0.5))
m4 = Movement(TimeGenerator.Exponential(1))

Movement.check()

# ---------------------------------------------------------------------
#                   Creating Loggers
# ---------------------------------------------------------------------
time_management.logger_set_list(ServiceStation.list)

# ---------------------------------------------------------------------
#                   Creating Preliminary FEL
# ---------------------------------------------------------------------
ief1.set_first_arrival(0)
ief2.set_first_arrival(0)
ief3.set_single_arrival(60)
ss1.set_rest_times([50, 110, 230, 290])
ss2.set_rest_times([50, 110, 230, 290])

# ---------------------------------------------------------------------
#                      Set Duration
# ---------------------------------------------------------------------
time_management.set_end_of_simulation(300)

# ---------------------------------------------------------------------
#                           RUN!
# ---------------------------------------------------------------------
try:
    while True:
        time_management.advance_time()
except time_management.SimulationDone:
    print("Simulation DONE!")
time_management.close_logger()
