import os
import sys
from provisionpad.db.database import load_database

def show_status():
    DB = load_database()
    print (DB)

if __name__ == "__main__":

    show_status()