import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
from aws.aws_ec2 import AWSec2Funcs
from db.database import load_database, save_database
from helpers.namehelpers import vpc_name
from helpers.texthelpers import write_into_text

     

def start_instance(boxname, DB):

    if boxname not in DB['stopped_instances']:
        print ('the box is not available check again:')
        sys.exit()

    region = os.environ['aws_region']
    home_folder = os.environ['my_home_folder']
    access_key = os.environ['aws_access_key_id']
    secret_key = os.environ['aws_secret_access_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)

    my_ssh_key_path = os.environ['my_ssh_key']
    ssh_key_name = my_ssh_key_path.strip().rsplit('/', 1)[-1].split('.')[0]

    id = DB['stopped_instances'][boxname]['id']
    DB['running_instances'][boxname] = awsf.start_ec2_instance(id)
    del(DB['stopped_instances'][boxname])
    # DB['available_names'].append(boxname)
    print (DB)
    save_database(DB)
    write_into_text(boxname,
'''
Host {0}
    HostName {1}
    User ubuntu
    IdentityFile {2}
    ForwardAgent yes
'''.format(boxname, DB['running_instances'][boxname]['public_ip'], my_ssh_key_path), 
os.path.join(home_folder,'.ssh/config'))

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
    start_instance(boxname, DB)