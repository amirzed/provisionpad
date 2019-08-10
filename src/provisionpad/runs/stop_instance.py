import os
import sys
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from provisionpad.db.database import load_database, save_database
from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.helpers.texthelpers import delete_text_from_file

     

def stop_instance(boxname, env_vars, DB):

    region = env_vars['aws_region']
    home_folder = env_vars['HOME']
    access_key = env_vars['access_key']
    secret_key = env_vars['secret_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)

    id = DB['running_instances'][boxname]['id']
    awsf.stop_ec2_instance(id)
    DB['stopped_instances'][boxname] = DB['running_instances'][boxname]
    del(DB['running_instances'][boxname])
    # DB['available_names'].append(boxname)
    save_database(DB, env_vars['db_path'])
    delete_text_from_file(boxname, os.path.join(home_folder,'.ssh/config'))

    print ('ec2 instance {0} stopped successfully'.format(boxname))

# if __name__ == "__main__":

#     import argparse
#     parser = argparse.ArgumentParser(description='A function to create instance', 
#                                      usage='%(prog)s [OPTIONS]')
#     parser.add_argument("-n", "--name", dest="boxname", default="", 
#                         help="Enter the name of the sandbox:")
#     args = parser.parse_args()
    
#     boxname = args.boxname

#     if not boxname:
#         print('Please enter the name of the box you want to remove')
#         sys.exit()

#     DB = load_database()
#     stop_instance(boxname, DB)