import os
import sys
import time
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from provisionpad.db.database import load_database, save_database
from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.helpers.texthelpers import write_into_text
from provisionpad.helpers.namehelpers import get_box_name
from provisionpad.helpers.update_status import update_status

def create_instance(boxname, boxtype, shut_down_time, env_vars, DB):

    update_status(env_vars,DB)

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
    # print (params)
    DB['running_instances'][boxname] = awsf.create_ec2_instance(params)
    # print (DB)
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

    tmp_dir = os.path.join(env_vars['env_dir'], 'tmp')
    tmp_tclock = os.path.join(tmp_dir,'tclock.py')
    tmp_cron = os.path.join(tmp_dir,'cron')

    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    write_into_text('timeer',
'''
import psutil
import time
import os
from os.path import expanduser
home = expanduser("~")
total_idlef = os.path.join(home, '.provisionpad/data/total_idle.out')
delta_idlef = os.path.join(home, '.provisionpad/data/delta_idle.out')
idle_time = psutil.cpu_times().idle
the_time  = time.time()
with open(total_idlef, 'r') as f:
    data = f.read().strip().split()
str = '%f %f' % (idle_time, the_time)
if len(data) != 2:
    with open(total_idlef, 'w') as f:
        f.write(str)
    with open(delta_idlef, 'w') as f:
        f.write('0\n')
else:
    idle_diff = (idle_time-float(data[0]))/(the_time-float(data[1]))
    with open(total_idlef, 'w') as f:
        f.write(str)
    with open(delta_idlef, 'a+') as f:
        f.write("%f\n" % idle_diff )  
with open(delta_idlef, 'r') as f:
    data = f.readlines()
    # if float(data[-1])>0.97 and abs(float(data[-1])-float(data[-2]))<0.002:
    #     os.system('sudo poweroff')
   
''',
tmp_tclock)

  

    with open(tmp_cron, 'wb') as f:
        towrite = '*/{0} * * * * python /home/ubuntu/.provisionpad/tclock.py\n'.format(shut_down_time)
        f.write(towrite.encode('UTF-8'))

    print ('Setting up auto power off in case of long idle time')
    time.sleep(30)

    os.system('ssh {0} pip install psutil'.format(boxname))
    os.system('ssh {0} mkdir .provisionpad'.format(boxname))
    os.system('ssh {0} mkdir .provisionpad/data'.format(boxname))
    os.system('ssh {0} touch ~/.provisionpad/data/total_idle.out'.format(boxname))
    # os.system('ssh {0} cat "" ~/.provisionpad/data/idle_log'.format(boxname))
    os.system('scp {0} {1}:~/.provisionpad/'.format(tmp_cron, boxname))
    os.system('scp {0} {1}:~/.provisionpad/'.format(tmp_tclock, boxname))
    os.system('ssh {0} crontab /home/ubuntu/.provisionpad/cron'.format(boxname))
    os.remove(tmp_cron)
    os.remove(tmp_tclock)




