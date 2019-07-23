import os
import sys
import pickle
from collections import deque

def initiate_db(dbpath):
    print('initiating the database')
    database = {'created_instances': 0}
    database['available_names'] = deque()
    database['running_instances'] = {}
    database['stopped_instances'] = {}
    pickle.dump( database, open( dbpath, 'wb' ), protocol=2 )
    return database

def load_database(dbpath):
    if os.path.isfile(dbpath):
        return pickle.load(open(dbpath, 'rb'))
    else: # used for initializing the database
        return initiate_db(dbpath)

def save_database(database, dbpath):
    pickle.dump( database, open( dbpath, 'wb' ), protocol=2 )
