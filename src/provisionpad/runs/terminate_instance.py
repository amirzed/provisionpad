import os
import sys
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from provisionpad.db.database import load_database, save_database
from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.helpers.texthelpers import delete_text_from_file


def terminate_instance(boxname, DB):

    region = os.environ['aws_region']
    home_folder = os.environ['my_home_folder']
    access_key = os.environ['aws_access_key_id']
    secret_key = os.environ['aws_secret_access_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)

    id = DB['running_instances'][boxname]['id']
    awsf.terminate_ec2_instance(id)
    del(DB['running_instances'][boxname])
    DB['available_names'].append(boxname)
    print (DB)
    save_database(DB)
    delete_text_from_file(boxname, os.path.join(home_folder,'.ssh/config'))

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='A function to create instance', 
                                     usage='%(prog)s [OPTIONS]')
    parser.add_argument("-n", "--name", dest="boxname", default="", 
                        help="Enter the name of the sandbox:")
    args = parser.parse_args()
    
    boxname = args.boxname

    if not boxname:
        print('Please enter the name of the box you want to remove')
        sys.exit()

    DB = load_database()
    terminate_instance(boxname, DB)