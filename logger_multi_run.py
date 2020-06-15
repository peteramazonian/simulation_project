import xlsxwriter
from datetime import datetime


class LoggerMR:
    def __init__(self, ss_names, replications):
        self.total_replications = replications
        self.ss_names = ss_names  # Setting list of service ServiceStations
        time = datetime.now().strftime("%d-%m-%Y--%H-%M-%S")
        self.wb = xlsxwriter.Workbook('LOG_MR/LOG-' + str(self.total_replications) + 'R--' + time + '.xlsx')  # Creating Excel report
        #  file in LOG_MR folder in the project directory
        self.ws = self.wb.add_worksheet("all logs")  # Creating a sheet inside the Excel file
        # Creating default format object
        self.default_format = self.wb.add_format(dict(font_name='Century Gothic', align='center', valign='vcenter'))
        # Defining a dictionary so it can be edited easily before creating a new format object
        self.header_format_dict = dict(font_name='Century Gothic', align='center', valign='vcenter', bold=True,
                                       font_color='navy', text_wrap=True, bg_color='silver', border=1)
        # Setting default format and height=14 for first 50 columns in all rows
        self.ws.set_column(0, 50, 14, self.default_format)
        # Freezing first 2 rows and first column
        self.ws.freeze_panes(2, 1)
        # Writing header for first column
        format_tmp = self.wb.add_format(self.header_format_dict)  # Creating a temporary format object
        self.ws.merge_range(0, 0, 1, 0, "Replication", format_tmp)  # Writing first row in merged cell
        # Writing header for column 2
        format_tmp = self.wb.add_format(self.header_format_dict)  # Creating a temporary format object
        format_tmp.set_bg_color('#CCFF99')  # Changing background color of the format object
        self.ws.write(0, 1, "System", format_tmp)  # Writing first row
        system_parameters = ['Average Time in System']
        for col_num, cell_name in enumerate(system_parameters):  # Writing second row
            self.ws.write(1, col_num + 1, cell_name, format_tmp)
        # Writing header for columns after 5
        # One section for each ServiceStation. It will cover all ServiceStations automatically.
        color_list = ['#FF5050', '#FFFF99']  # Defining a color list to choose in a loop for each
        # ServiceStation so it can be separated easily
        for num, ss in enumerate(self.ss_names):
            format_tmp = self.wb.add_format(self.header_format_dict)
            format_tmp.set_bg_color(color_list[int(num % len(color_list))])  # Setting background color of the
            # format object used for this ServiceStation's header, from the color list
            # Parameters names list. you need to edit this if you want to change what parameters are printed in log file
            # Also you should change ServiceStation's "final_calculations" function
            # Order of parameters in ss_parameters and result dict in ServiceStations should be the same
            ss_parameters = ['Total Wait Time', 'Average Queue Delay', 'Average Queue Length', 'Maximum Queue Length',
                             'Servers Efficiency', 'Queue Busy Percentage']
            i = num * len(ss_parameters) + 2    # Choose starting column
            self.ws.merge_range(0, i, 0, i + len(ss_parameters) - 1, ss, format_tmp)   # Writing first row in
            # merged cell
            for index, cell_name in enumerate(ss_parameters):   # Writing second row
                self.ws.write(1, index + i, cell_name, format_tmp)

        self.row = 2    # Setting the starting row to write logs. 3rd row is the row after header.
        self.replication_number = 1

    def replication_logger(self, s_list, SystemArrival):  # It will write the system evaluation parameters for each replication in a new row
        column = 0
        format_tmp = self.wb.add_format(self.header_format_dict)  # Creating a temporary format object
        self.ws.write(self.row, column, self.replication_number, format_tmp)
        self.replication_number += 1
        column += 1
        for key, value in SystemArrival.result.items():
            self.ws.write(self.row, column, value)
            column += 1
        for ss in s_list:
            for key, value in ss.result.items():
                self.ws.write(self.row, column, value)
                column += 1
        self.row += 1

    def result_logger(self, ss_names, result):    # It will write the system evaluation parameters in a table at the end of the log file
        self.row += 3   # The table starts 3 rows after where log table ends
        column = 4  # The table starts from 5th column
        format_tmp = self.wb.add_format(self.header_format_dict)    # Creating a temporary format object
        format_tmp.set_bg_color('#29A8FF')  # Changing it's background color to blue
        # Writing the header:
        self.ws.write(self.row, column, 'Scope', format_tmp)
        self.ws.merge_range(self.row, column + 1, self.row, column + 2, "Parameter Average", format_tmp)
        self.ws.write(self.row, column + 3, 'Value', format_tmp)
        self.row += 1
        color_list = ['#FF5050', '#FFFF99']     # Used to separate parts with two colors in loop
        for num, ss in enumerate(ss_names):  # Writing ServiceStations evaluation parameters
            format_tmp = self.wb.add_format(self.header_format_dict)
            format_tmp.set_bg_color(color_list[int(num % len(color_list))])
            if len(result[num]) > 1:
                self.ws.merge_range(self.row, column, self.row + len(result[num]) - 1, column, ss, format_tmp)
            else:
                self.ws.write(self.row, column, ss, format_tmp)
            for key, value in result[num].items():   # Writing parameters name and value
                self.ws.merge_range(self.row, column + 1, self.row, column + 2, key, format_tmp)
                self.ws.write(self.row, column + 3, value / self.total_replications, format_tmp)
                self.row += 1

    def close_file(self):   # It will close and save the Excel file in the project directory
        self.wb.close()


