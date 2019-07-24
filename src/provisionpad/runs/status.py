from __future__ import print_function

from colorclass import Color, Windows

from terminaltables import SingleTable
from provisionpad.helpers.update_status import update_status

def table_server_timings(DB):
    """Return table string to be printed."""
    table_data = [[Color('{autogreen}Name{/autogreen}'), 'Type', 'Info']]
    for ins, ins_val in DB['running_instances'].items():
        table_data.append([Color('{autogreen}{0}{/autogreen}').format(ins), ins_val['type'], 'to ssh do'])
    # table_data = [
    #     [Color('{autogreen}<10ms{/autogreen}'), '192.168.0.100, 192.168.0.101'],
    #     [Color('{autoyellow}10ms <= 100ms{/autoyellow}'), '192.168.0.102, 192.168.0.103'],
    #     [Color('{autored}>100ms{/autored}'), '192.168.0.105'],
    # ]
    table_instance = SingleTable(table_data, 'us-east-2')
    table_instance.inner_heading_row_border = True
    return table_instance.table

def show_status(env_vars, DB):
    update_status(env_vars,DB)
    print (DB)
    table = table_server_timings(DB)
    print (table)










