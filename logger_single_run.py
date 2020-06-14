import xlsxwriter
from datetime import datetime


class LoggerSR:
    def __init__(self, s_list):
        self.s_list = s_list  # Setting list of service ServiceStations
        self.system_arrival = __import__('system_arrival').SystemArrival  # Importing SystemArrival class. It
        # should be imported inside init to avoid circular imports
        time = datetime.now().strftime("%d-%m-%Y--%H-%M-%S")
        self.wb = xlsxwriter.Workbook('LOG_SR/LOG-SR--' + time + '.xlsx')  # Creating Excel report file in LOG_SR
        # folder in the project directory
        self.ws = self.wb.add_worksheet("all logs")  # Creating a sheet inside the Excel file
        # Creating default format object
        self.default_format = self.wb.add_format(dict(font_name='Century Gothic', align='center', valign='vcenter'))
        # Defining a dictionary so it can be edited easily before creating a new format object
        self.header_format_dict = dict(font_name='Century Gothic', align='center', valign='vcenter', bold=True,
                                       font_color='navy', text_wrap=True, bg_color='silver', border=1)
        # Setting default format and height=14 for first 50 columns in all rows
        self.ws.set_column(0, 50, 14, self.default_format)
        # Freezing first 2 rows and first 3 columns
        self.ws.freeze_panes(2, 3)
        # Writing header for first 3 columns
        format_tmp = self.wb.add_format(self.header_format_dict)  # Creating a temporary format object
        self.ws.merge_range(0, 0, 0, 2, "FEL", format_tmp)  # Writing first row in merged cell
        fel_parameters = ["Clock", "Event Type", "Costumer_ID"]
        for col_num, cell_name in enumerate(fel_parameters):  # Writing second row
            self.ws.write(1, col_num, cell_name, format_tmp)
        # Writing header for columns 4-5
        format_tmp = self.wb.add_format(self.header_format_dict)  # Creating a temporary format object
        format_tmp.set_bg_color('#CCFF99')  # Changing background color of the format object
        self.ws.merge_range(0, 3, 0, 4, "System", format_tmp)  # Writing first row in merged cell
        system_parameters = ["Costumers Total Time", "Costumers Departured"]
        for col_num, cell_name in enumerate(system_parameters):  # Writing second row
            self.ws.write(1, col_num + 3, cell_name, format_tmp)
        # Writing header for columns after 5
        # One section for each ServiceStation. It will cover all ServiceStations automatically.
        color_list = ['#FF5050', '#FFFF99']  # Defining a color list to choose in a loop for each
        # ServiceStation so it can be separated easily
        for num, ss in enumerate(self.s_list):
            format_tmp = self.wb.add_format(self.header_format_dict)
            format_tmp.set_bg_color(color_list[int(num % len(color_list))])  # Setting background color of the
            # format object used for this ServiceStation's header, from the color list
            # Parameters names list. you need to edit this if you want to change what parameters are printed in log file
            # Also you should change ServiceStation's "return_printables" function
            # Order of parameters in ss_parameters and printables list in ServiceStations should be the same
            ss_parameters = ['Available Servers', 'Busy Servers', 'Queue Len', 'Rest in Waiting',
                             'Cumulative Queue Len', 'Max Queue Len', 'Total Service Time', 'Total Service Count',
                             'Queue Delay Cumulative', 'Queue Total Time', 'Servers Total Busy Time',
                             'Servers Total Available Time']
            i = num * len(ss_parameters) + 5    # Choose starting column
            self.ws.merge_range(0, i, 0, i + len(ss_parameters) - 1, ss.name, format_tmp)   # Writing first row in
            # merged cell
            for index, cell_name in enumerate(ss_parameters):   # Writing second row
                self.ws.write(1, index + i, cell_name, format_tmp)

        self.row = 2    # Setting the starting row to write logs. 3rd row is the row after header.

    def fel_logger(self, event_notice):     # It will write the event notice passed, into in the next blank row
        for col_num, item in enumerate(event_notice[0: -1]):
            self.ws.write(self.row, col_num, item)
        self.variable_logger()  # Calling variable_logger function to log cumulative and state variables
        self.row += 1   # Moving to next row

    def variable_logger(self):  # It will log cumulative and state variables for SystemArrivals and ServiceStations in
        # columns after 3 (where fel ends)
        column = 3
        # Writing System variables
        self.ws.write(self.row, column, self.system_arrival.costumers_total_time)
        column += 1
        self.ws.write(self.row, column, self.system_arrival.costumers_departured)
        column += 1
        # Writing ServiceStation variables
        for ss in self.s_list:
            for item in ss.return_printables():
                self.ws.write(self.row, column, item)
                column += 1

    def result_logger(self):    # It will write the system evaluation parameters in a table at the end of the log file
        self.row += 3   # The table starts 3 rows after where log table ends
        column = 4  # The table starts from 5th column
        format_tmp = self.wb.add_format(self.header_format_dict)    # Creating a temporary format object
        format_tmp.set_bg_color('#29A8FF')  # Changing it's background color to blue
        # Writing the header:
        self.ws.write(self.row, column, 'Scope', format_tmp)
        self.ws.merge_range(self.row, column + 1, self.row, column + 2, "Parameter", format_tmp)
        self.ws.write(self.row, column + 3, 'Value', format_tmp)
        self.row += 1
        color_list = ['#FF5050', '#FFFF99']     # Used to separate parts with two colors in loop
        for num, ss in enumerate(self.s_list):  # Writing ServiceStations evaluation parameters
            format_tmp = self.wb.add_format(self.header_format_dict)
            format_tmp.set_bg_color(color_list[int(num % len(color_list))])
            result = ss.result  # ss.result is calculated in final_calculations method in ServiceStations at the end
            # of simulation
            self.ws.merge_range(self.row, column, self.row + len(result) - 1, column, ss.name, format_tmp)
            for key, value in result.items():   # Writing parameters name and value
                self.ws.merge_range(self.row, column + 1, self.row, column + 2, key, format_tmp)
                self.ws.write(self.row, column + 3, value, format_tmp)
                self.row += 1
        # Writing ServiceStations evaluation parameters:
        result = self.system_arrival.result     # SystemArrival.result is calculated in final_calculations method in
        # SystemArrival at the end of simulation
        format_tmp = self.wb.add_format(self.header_format_dict)
        self.ws.write(self.row, column, "System", format_tmp)   # Writing the scope column
        for key, value in result.items():   # Writing parameters name and value
            self.ws.merge_range(self.row, column + 1, self.row, column + 2, key, format_tmp)
            self.ws.write(self.row, column + 3, value, format_tmp)
            self.row += 1

    def close_file(self):   # It will close and save the Excel file in the project directory
        self.wb.close()
