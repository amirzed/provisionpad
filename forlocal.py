# Create a *.pth file and add the absolute path of the package for local testing
# I found this to be the easiest way -- Amir

import sys
import os

from os.path import expanduser
home = expanduser("~")

# def create_aliases():
#     env_dir = os.path.join(home, '.provisionpad') 
#     if not os.path.isdir(env_dir):
#         os.mkdir(env_dir)
#     if os.path.isfile(os.path.join(env_dir, 'aliases')):
#         thein = input ('It seems you already have aliases'
#                        'Do you want to replace it? (y/n): ')
#         if thein.strip()=='y':
#             os.remove(os.path.join(env_dir, 'aliases'))
#         elif thein.strip() == 'n':
#             return 
#         else:
#             print('Invalid input')
#             sys.exit()

#     rootpath = os.path.dirname(os.path.realpath(__file__))
#     thebin = os.path.join(rootpath,'bin/ppad')

#     with open(os.path.join(env_dir, 'aliases'), 'w') as f:
#         f.write('alias ppad=\''+thebin+'\'')
# create_aliases()