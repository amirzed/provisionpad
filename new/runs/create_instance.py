import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
from aws.aws_ec2 import AWSec2Funcs
from db.database import load_database, save_database
from helpers.namehelpers import vpc_name
from helpers.texthelpers import write_into_text


def get_box_name(DB):
    """
    gets redis variables names and returns the best name for the
    newly created instance
    """
    if len(DB['available_names']) > 0:
        dname = DB['available_names'].popleft()
        if dname in DB['running_instances'] or\
                dname in DB['stopped_instances'] :
            print ('something wrong in this function fix me')
            sys.exit()
        boxn = dname
    else:
        boxi = DB['created_instances'] + 1
        boxn = 'box{0}'.format(boxi)
        DB['created_instances'] += 1
        save_database(DB)
    return boxn
        

def start_instance(boxname, boxtype, DB):

    DB = load_database()

    region = os.environ['aws_region']
    home_folder = os.environ['my_home_folder']
    access_key = os.environ['aws_access_key_id']
    secret_key = os.environ['aws_secret_access_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)

    my_ssh_key_path = os.environ['my_ssh_key']
    ssh_key_name = my_ssh_key_path.strip().rsplit('/', 1)[-1].split('.')[0]

    vpcname = vpc_name()

    if not boxname:
        boxname = get_box_name(DB)
    else:
        if boxname[:3] == 'box' or \
                boxname in DB['runnin_instances'] or \
                boxname in DB['stopped_instances']:
            print ("enter a better name. either exists or starts with box")
            sys.exit()

    params = {}
    params['ssh_key_name'] = ssh_key_name
    params['aws_ami'] = os.environ['aws_ami']
    params['aws_iam_role'] = os.environ['iam_role']
    params['vpc'] = DB[vpcname]
    params['box_type'] = boxtype
    params['name'] = os.environ['your_name'].replace(" ", "")+boxname

    DB[boxname] = awsf.create_ec2_instance(params)
    DB['running_instances'].add(boxname)
    print (DB['running_instances'])
    write_into_text(boxname,
'''
Host {0}
    HostName {1}
    User ubuntu
    IdentityFile {2}
    ForwardAgent yes
'''.format(boxname, DB[boxname]['public_ip'], my_ssh_key_path), 
os.path.join(home_folder,'.ssh/config'))
    save_database(DB)



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='A function to create instance', 
                                     usage='%(prog)s [OPTIONS]')
    parser.add_argument("-n", "--name", dest="boxname", default="", 
                        help="Enter the name of the sandbox:")
    parser.add_argument("-t", "--type", dest="boxtype", default="t2.micro", 
                        help="The type of instance. For example for ec2 t2.micro blah blah")
    args = parser.parse_args()
    
    boxname = args.boxname
    boxtype = args.boxtype

    DB = load_database()
    start_instance(boxname, boxtype, DB)