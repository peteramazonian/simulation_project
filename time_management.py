import bisect
from logger import Logger

fel = []
clock = 0
logger = None


def logger_set_list(s_list):
    global logger
    logger = Logger(s_list)


def add_to_fel(event_notice: tuple):
    try:
        bisect.insort_left(fel, event_notice)
    except TypeError as ERR:
        fel.append(event_notice)
        fel.sort(key=lambda x: x[0])


class SimulationDone(Exception):
    pass


def es(*args):
    raise SimulationDone


def set_end_of_simulation(es_time):
    add_to_fel((es_time, es))


def postponed_rest_log_editor():
    # TODO edit
    pass


def advance_time():
    global clock
    tmp = fel[0]  # Using tmp and delete the event notice from fel before handling it is necessary when we want to add
    # event notices to the current clock. E.g. when moving time between two parts equals 0
    del fel[0]
    clock = tmp[0]
    tmp[-1](tmp[-2])
    logger.fel_logger(tmp)


def close_logger():
    logger.close_file()
