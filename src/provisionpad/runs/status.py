from __future__ import print_function

from colorclass import Color, Windows

from terminaltables import SingleTable
from provisionpad.helpers.update_status import update_status

class StatTable:

    def __init__(self, instance_status, color):
        self.color = color
        self.instance_status = instance_status

    def stat(self, DB):
        """Return table string to be printed."""
        table_data = [[Color('{'+self.color+'}Name{/'+self.color+'}'), 'Type', 'SSH']]
        for ins, ins_val in DB[self.instance_status].items():
            table_data.append([Color('{'+self.color+'}'+ins+'{/'+self.color+'}'), 
                                ins_val['type'], 'ssh {0}'.format(ins)])
        table_instance = SingleTable(table_data)
        table_instance.inner_heading_row_border = True
        return table_instance.table

def show_status(env_vars, DB):
    update_status(env_vars,DB)
    # print (DB)
    table_running = StatTable('running_instances', 'autogreen')
    table_stopped = StatTable('stopped_instances', 'autoyellow')
    print (table_running.stat(DB))
    print (table_stopped.stat(DB))










