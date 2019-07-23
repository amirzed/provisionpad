import os
import sys
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from provisionpad.db.database import load_database, save_database
from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.helpers.texthelpers import write_into_text


def get_box_name(DB, dbpath):
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
        save_database(DB, dbpath)
    return boxn
        

def create_instance(boxname, boxtype, env_vars, DB):

    region = env_vars['aws_region']
    home_folder = env_vars['HOME']
    access_key = env_vars['access_key']
    secret_key = env_vars['secret_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)

    my_ssh_key_path = env_vars['key_pair_path']
    ssh_key_name = env_vars['key_pair_name']

    if not boxname:
        boxname = get_box_name(DB, env_vars['db_path'])
    else:
        if boxname[:3] == 'box' or \
                boxname in DB['runnin_instances'] or \
                boxname in DB['stopped_instances']:
            print ("enter a better name. either exists or starts with box")
            sys.exit()

    params = {}
    params['ssh_key_name'] = ssh_key_name
    params['aws_ami'] = env_vars['aws_ami']
    params['aws_iam_role'] = env_vars['role_name']
    params['vpc'] = DB[env_vars['vpc_name'] ]
    params['box_type'] = boxtype
    params['name'] = env_vars['your_name']+boxname

    # DB[boxname] = awsf.create_ec2_instance(params)
    print (params)
    DB['running_instances'][boxname] = awsf.create_ec2_instance(params)
    print (DB)
    write_into_text(boxname,
'''
Host {0}
    HostName {1}
    User ubuntu
    IdentityFile {2}
    ForwardAgent yes
'''.format(boxname, DB['running_instances'][boxname]['public_ip'], my_ssh_key_path), 
os.path.join(home_folder,'.ssh/config'))
    save_database(DB, env_vars['db_path'])



# if __name__ == "__main__":

#     import argparse
#     parser = argparse.ArgumentParser(description='A function to create instance', 
#                                      usage='%(prog)s [OPTIONS]')
#     parser.add_argument("-n", "--name", dest="boxname", default="", 
#                         help="Enter the name of the sandbox:")
#     parser.add_argument("-t", "--type", dest="boxtype", default="t2.micro", 
#                         help="The type of instance. For example for ec2 t2.micro blah blah")
#     args = parser.parse_args()
    
#     boxname = args.boxname
#     boxtype = args.boxtype

#     DB = load_database()
#     create_instance(boxname, boxtype, DB)