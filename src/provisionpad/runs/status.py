import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
from db.database import load_database

def show_status():
    DB = load_database()
    print (DB)

if __name__ == "__main__":

    show_status()