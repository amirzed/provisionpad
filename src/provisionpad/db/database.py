import os
import sys
import pickle
from collections import deque
env_var_dir = os.environ['env_var_dir']
sys.path.append(env_var_dir)
database_name = os.path.join(env_var_dir, 'database.p')

def initiate_db():
    print('initiating the database')
    database = {'created_instances': 0}
    database['available_names'] = deque()
    database['running_instances'] = {}
    database['stopped_instances'] = {}
    pickle.dump( database, open( database_name, 'wb' ), protocol=2 )
    return database

def load_database():
    if os.path.isfile(database_name):
        return pickle.load(open(database_name, 'rb'))
    else: # used for initializing the database
        return initiate_db()

def save_database(database):
    pickle.dump( database, open( database_name, 'wb' ), protocol=2 )
