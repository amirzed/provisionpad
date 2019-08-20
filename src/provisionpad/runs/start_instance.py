import os
import sys
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from provisionpad.db.database import load_database, save_database
from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.helpers.texthelpers import write_into_text



def start_instance(boxname, env_vars, DB):

    if boxname not in DB['stopped_instances']:
        print ('the box is not available check again:')
        sys.exit()


    print ('Waiting for confirmation from AWS')
    region = env_vars['aws_region']
    home_folder = env_vars['HOME']
    access_key = env_vars['access_key']
    secret_key = env_vars['secret_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)

    my_ssh_key_path = env_vars['key_pair_path']
    ssh_key_name = env_vars['key_pair_name']

    id = DB['stopped_instances'][boxname]['id']
    DB['running_instances'][boxname] = awsf.start_ec2_instance(id)
    DB['running_instances'][boxname]['sdrive'] = DB['stopped_instances'][boxname]['sdrive']
    del(DB['stopped_instances'][boxname])
    # DB['available_names'].append(boxname)
    save_database(DB, env_vars['db_path'])
    write_into_text(boxname,
'''
Host {0}
    HostName {1}
    User ubuntu
    IdentityFile {2}
    ForwardAgent yes
    StrictHostKeyChecking no
'''.format(boxname, DB['running_instances'][boxname]['public_ip'], my_ssh_key_path),
os.path.join(home_folder,'.ssh/config'))

    print ('ec2 instance {0} started successfully'.format(boxname))
