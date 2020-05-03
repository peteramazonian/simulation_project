import bisect

fel = []
def add_to_fel(event_notice : tuple):
    try:
        bisect.insort_left(fel, event_notice)
    except TypeError as ERR:
        fel.append(event_notice)
        fel.sort(key = lambda x: x[0])
