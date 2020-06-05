import xlsxwriter


class Logger:
    def __init__(self, s_list):
        self.s_list = s_list
        self.system_arrival = __import__('system_arrival').SystemArrival
        self.wb = xlsxwriter.Workbook('log.xlsx')
        self.ws = self.wb.add_worksheet("all logs")
        self.default_format = self.wb.add_format(dict(font_name='Century Gothic', align='center', valign='vcenter'))
        self.header_format_dict = dict(font_name='Century Gothic', align='center', valign='vcenter', bold=True,
                                       font_color='navy', text_wrap=True, bg_color='silver', border=1)
        # self.ws.set_row(0, None, self.header_format)
        # self.ws.set_row(1, None, self.header_format)
        self.ws.set_column(0, 50, 14, self.default_format)
        self.ws.freeze_panes(2, 3)
        # 1
        format_tmp = self.wb.add_format(self.header_format_dict)
        self.ws.merge_range(0, 0, 0, 2, "FEL", format_tmp)
        fel_parameters = ["Clock", "Event Type", "Costumer_ID"]
        for col_num, cell_name in enumerate(fel_parameters):
            self.ws.write(1, col_num, cell_name, format_tmp)
        # 2
        format_tmp = self.wb.add_format(self.header_format_dict)
        format_tmp.set_bg_color('#CCFF99')
        self.ws.merge_range(0, 3, 0, 4, "System", format_tmp)
        system_parameters = ["Costumers Total Time", "Costumers Departured"]
        for col_num, cell_name in enumerate(system_parameters):
            self.ws.write(1, col_num + 3, cell_name, format_tmp)
        # 3
        for num, item in enumerate(self.s_list):
            color_list = ['#FF5050', '#FFFF99']
            format_tmp = self.wb.add_format(self.header_format_dict)
            format_tmp.set_bg_color(color_list[int(num % len(color_list))])
            ss_parameters = ['Available Servers', 'Busy Servers', 'Queue Len', 'Rest in Waiting',
                             'Cumulative Queue Len', 'Max Queue Len', 'Total Service Time', 'Total Service Count',
                             'Servers Total Busy Time', 'Servers Total Available Time']
            i = num * len(ss_parameters) + 5
            self.ws.merge_range(0, i, 0, i + len(ss_parameters) - 1, item.name, format_tmp)
            for index, cell_name in enumerate(ss_parameters):
                self.ws.write(1, index + i, cell_name, format_tmp)

        self.row = 2

    def fel_logger(self, event_notice):
        for col_num, item in enumerate(event_notice[0: -1]):
            self.ws.write(self.row, col_num, item)
        self.variable_logger()
        self.row += 1

    def variable_logger(self):
        column = 3
        self.ws.write(self.row, column, self.system_arrival.costumers_total_time)
        column += 1
        self.ws.write(self.row, column, self.system_arrival.costumers_departured)
        column += 1
        for ss in self.s_list:
            for item in ss.return_printables():
                self.ws.write(self.row, column, item)
                column += 1

    def final_calculations(self):
        pass

    def close_file(self):
        self.wb.close()

