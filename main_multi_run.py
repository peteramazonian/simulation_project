import sys
import importlib
from service_station import ServiceStation
from system_arrival import SystemArrival
from movement import Movement
from time_generator import TimeGenerator
from number_generator import NumberGenerator
import time_management
from logger_multi_run import LoggerMR


replications = 100
result = []
ss_names = ['ss1', 'ss2', 'ss3']
logger = LoggerMR(ss_names, replications)
i = 0
while i < replications:
    importlib.reload(sys.modules['service_station'])
    importlib.reload(sys.modules['system_arrival'])
    importlib.reload(sys.modules['movement'])
    importlib.reload(sys.modules['time_management'])

    from service_station import ServiceStation
    from system_arrival import SystemArrival
    from movement import Movement

    # Its our simulation's main file.
    # Here we import classes and functions from other project files.
    # Then we need to make objects from our classes and set attributes.
    # These objects are used to setup the system in a modular way.
    # You can make as many service stations as you need with their own attributes, then arrange the whole system

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
    es = 300
    time_management.set_end_of_simulation(es)

    # ---------------------------------------------------------------------
    #                           RUN!
    # ---------------------------------------------------------------------
    try:
        while True:
            time_management.advance_time()
    except time_management.SimulationDone:
        for ss in ServiceStation.list:
            ss.final_calculations()
        SystemArrival.final_calculations()
        logger.replication_logger(ServiceStation.list, SystemArrival)
        i += 1
        print('#' + str(i) + '  :  Simulation DONE!')

    if i == 1:
        for ss in ServiceStation.list:
            result.append(ss.result)
        result.append(SystemArrival.result)
    else:
        for j, ss in enumerate(ServiceStation.list):
            for key, value in ss.result.items():
                result[j][key] += value
        for key, value in SystemArrival.result.items():
            result[-1][key] += value


ss_names.append('System')
for num, scope in enumerate(result):
    for key, value in scope.items():
        print("%s:  %s  =  %s" %(ss_names[num], key, round(value / replications, 10)))
logger.result_logger(ss_names, result)
logger.close_file()


