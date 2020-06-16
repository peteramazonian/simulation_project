import bisect


# ----------------------------------------------------------------------------------------------------------------
# In this module we handle anything related to FEL and clock. in another word this module is the engine that makes
# the code to move.
# ----------------------------------------------------------------------------------------------------------------


fel = []    # It's our simulation's main Future Event List.
clock = 0   # It is the clock that we are in it right now, trying to handle future events and advance time.


def add_to_fel(event_notice: tuple):    # This func will add a given tuple to our FEL, in the right place based on
    # event's clock.
    try:
        bisect.insort_left(fel, event_notice)   # Bisect library provides a very efficient algorithm to add an object
        # in the right place in a SORTED list of objects to keep it sorted.
    except TypeError:   # It will be used when two tuples are very exactly same except their functions passed.
        # bisect cant compare functions so it will return an error. After all it's some how impossible for two events
        # to be that much same.
        fel.append(event_notice)
        fel.sort(key=lambda x: x[0])


class SimulationDone(Exception):    # It's an exception class that will raise the SimulationDone exception when we want.
    pass


def es(*args):  # es is short form for End of Simulation. It will throw "SimulationDone" Exception when called.
    raise SimulationDone


def set_end_of_simulation(es_time):     # It will add an "es" event to the fel at clock = es_time
    add_to_fel((es_time, es))


def advance_time():     # This function will check the FEL, and handle the very upcoming event and advances the clock.
    global clock
    tmp = fel[0]  # Using tmp and delete the event notice from fel before handling it is necessary when we want to add
    # event notices to the current clock. E.g. when moving time between two parts equals 0
    del fel[0]
    clock = tmp[0]  # Sets the clock to current event's clock.
    tmp[-1](tmp[-2])    # Calls the event notice's method which is placed in the last element of the tuple, with passing
    # the one before the last element as it's argument. the argument is mostly the user_ID
    return tmp  # It will return the event notice just handled to the main file. it's used to log the event notice.
