from __future__ import print_function

from colorclass import Color, Windows

from terminaltables import SingleTable
from provisionpad.helpers.update_status import update_status
import sys

class StatTable:

    def __init__(self, instance_status, color):
        self.color = color
        self.instance_status = instance_status

    def stat(self, DB):
        """Return table string to be printed."""
        table_data = [[Color('{'+self.color+'}Name{/'+self.color+'}'), 'Type', 'Volumes', 'SSH']]
        for ins, ins_val in DB[self.instance_status].items():
            volume = 'root;'
            for _, val in ins_val['sdrive'].items():
                volume += ' {0} GB;'.format(val['size'])
            table_data.append([Color('{'+self.color+'}'+ins+'{/'+self.color+'}'),
                                ins_val['type'], volume,'ssh {0}'.format(ins)])
        table_instance = SingleTable(table_data, self.instance_status)
        table_instance.inner_heading_row_border = True
        return table_instance.table

    def sstat(self, DB):
        """Return table string to be printed."""
        str_to_return  = '\n'+self.instance_status+'\n'
        str_to_return += ' ' *len(self.instance_status) + \
                   "{:<20} {:<20} {:<20} {:<20}\n".format('Name', 'Type', 'Volumes', 'SSH')
        for ins, ins_val in DB[self.instance_status].items():
            volume = 'root;'
            for _, val in ins_val['sdrive'].items():
                volume += ' {0} GB;'.format(val['size'])
            str_to_return += ' ' *len(self.instance_status) + \
                   "{:<20} {:<20} {:<20} {:<20}\n".format(ins, ins_val['type'], volume, 'ssh {0}\n'.format(ins))
        str_to_return += '\n'
        return str_to_return

def show_status(env_vars, DB):
    update_status(env_vars,DB)
    # print (DB)
    table_running = StatTable('running_instances', 'autogreen')
    table_stopped = StatTable('stopped_instances', 'autoyellow')
    if sys.platform == 'win32':
        print (table_running.sstat(DB))
        print (table_stopped.sstat(DB))
    else:
        print (table_running.stat(DB))
        print (table_stopped.stat(DB))










