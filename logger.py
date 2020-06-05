import xlsxwriter

class Logger:
    def __init__(self, s_list):
        self.s_list = s_list
        self.wb = xlsxwriter.Workbook('log.xlsx')
        self.ws = self.wb.add_worksheet("all logs")
        self.default_format = self.wb.add_format(dict(font_name='Century Gothic', align='center', valign='vcenter'))
        self.header_format = self.wb.add_format(
            dict(font_name='Century Gothic', align='center', valign='vcenter', bold=True, font_color='navy',
                 text_wrap=True, bg_color='silver', border=1))
        self.ws.set_row(0, None, self.header_format)
        self.ws.set_row(1, None, self.header_format)
        self.ws.set_column(0, 50, 14, self.default_format)
        self.ws.freeze_panes(2, 0)
        # 1
        self.ws.merge_range(0, 0, 0, 2, "FEL")
        fel_parameters = ["Clock", "Event Type", "Costumer_ID"]
        for col_num, cell_name in enumerate(fel_parameters):
            self.ws.write(1, col_num, cell_name)
        # 2
        self.header_format.set_bg_color('#FFFF99')
        self.ws.merge_range(0, 3, 0, 4, "System")
        system_parameters = ["Costumers Total Time", "Costumers Departured"]
        for col_num, cell_name in enumerate(system_parameters):
            self.ws.write(1, col_num + 3, cell_name, self.header_format)
        # 3
        for num, item in enumerate(s_list):
            color_list = ['#FF5050', '#FFFF99']
            header_format = self.wb.add_format(
                dict(font_name='Century Gothic', align='center', valign='vcenter', bold=True, font_color='navy',
                     text_wrap=True, bg_color=color_list[int(num % len(color_list))], border=1))
            ss_parameters = ['Available Servers', 'Busy Servers', 'Queue Len', 'Rest in Waiting',
                             'Cumulative Queue Len', 'Max Queue Len', 'Total Service Time', 'Total Service Count',
                             'Servers Total Busy Time', 'Servers Total Available Time']
            i = num * len(ss_parameters) + 5
            self.ws.merge_range(0, i, 0, i + len(ss_parameters) - 1, item.name, header_format)
            for index, cell_name in enumerate(ss_parameters):
                self.ws.write(1, index + i, cell_name, header_format)


    def fel_logger(self, event_notice):

        self.variable_logger()
        pass

    def variable_logger(self):
        pass

    def final_calculations(self):
        pass

    def close_file(self):
        self.wb.close()

