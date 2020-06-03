import bisect
import xlwt


fel = []
clock = 0


wb = xlwt.Workbook()    # Creating a new Workbook object to write data to excel
log = wb.add_sheet("FEL Log", cell_overwrite_ok=True)
log.write(0, 0, "Time")
log.write(0, 1, "Event Type")
log.write(0, 2, "Costumer ID")
row = 0


def fel_logger(event_notice):
    global log, row
    col = 0
    for item in event_notice[0 : -1]:
        log.write(row, col, item)
        col += 1
    row += 1


def add_to_fel(event_notice: tuple):
    try:
        bisect.insort_left(fel, event_notice)
    except TypeError as ERR:
        fel.append(event_notice)
        fel.sort(key=lambda x: x[0])


def postponed_rest_log_editor():
    global row
    row -= 1


def advance_time():
    global clock, log
    tmp = fel[0]    # Using tmp and delete the event notice from fel before handling it is necessary when we want to add
    # event notices to the current clock. E.g. when moving time between two parts equals 0
    del fel[0]
    clock = tmp[0]
    fel_logger(tmp)
    tmp[-1](tmp[-2])


def close_logger():
    global wb
    wb.save("log.xls")

