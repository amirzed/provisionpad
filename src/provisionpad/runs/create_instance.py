import os
import sys
import time
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from provisionpad.db.database import load_database, save_database
from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.helpers.texthelpers import write_into_text
from provisionpad.helpers.namehelpers import get_box_name

def create_instance(boxname, boxtype, shut_down_time, env_vars, DB):

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
                boxname in DB['running_instances'] or \
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
    StrictHostKeyChecking no
'''.format(boxname, DB['running_instances'][boxname]['public_ip'], my_ssh_key_path), 
os.path.join(home_folder,'.ssh/config'))
    save_database(DB, env_vars['db_path'])


    write_into_text('timeer',
'''
import psutil
idle_time = psutil.cpu_times().idle
import os
with open('/home/ubuntu/test.file', 'w') as f:
    f.write('idle time: {0}, total_time: {1}, ratio: {2}'.format(idle_time, float({1}), idle_time/float({2})))
if idle_time/float({0})>0.95:
    os.system('sudo poweroff')
'''.format(shut_down_time*60, shut_down_time*60, shut_down_time*60),
'/tmp/tclock.py')

#     write_into_text('timeer',
# '''
# * * * * * python /home/ubuntu/.provisionpad/tclock.py
# ''',
# '/tmp/mycron')
    with open('/tmp/mycron', 'w') as f:
        f.write('*/{0} * * * * python /home/ubuntu/.provisionpad/tclock.py\n'.format(shut_down_time))

    print ('going to sleep')
    time.sleep(60)
    print ('going to wake up')

    os.system('ssh {0} pip install psutil'.format(boxname))
    os.system('ssh {0} mkdir .provisionpad'.format(boxname))
    os.system('scp /tmp/tclock.py {0}:~/.provisionpad/'.format(boxname))
    os.system('scp /tmp/mycron {0}:~/.provisionpad/'.format(boxname))
    os.system('ssh {0} crontab /home/ubuntu/.provisionpad/mycron'.format(boxname))
    os.system('rm -rf /tmp/mycron')
    os.system('rm -rf /tmp/tclock.py')





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