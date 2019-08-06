import os
import sys
from provisionpad.db.database import save_database


def vpc_name():
    return os.environ['your_name'].replace(" ", "")+'_VPC'


def get_box_name(DB, dbpath):
    """
    gets redis variables names and returns the best name for the
    newly created instance
    """
    if len(DB['available_names']) > 0:
        dname = DB['available_names'].popleft()
        if dname in DB['running_instances'] or\
                dname in DB['stopped_instances'] :
            raise Exception('Was not able to find a proper name. Please report the bug')
        boxn = dname
    else:
        boxi = DB['created_instances'] + 1
        boxn = 'box{0}'.format(boxi)
        DB['created_instances'] += 1
        save_database(DB, dbpath)
    return boxn