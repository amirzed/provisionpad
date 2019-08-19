import sys
import os
from provisionpad.aws.aws_vol import AWSvolFuncs
from provisionpad.db.database import load_database, save_database
from provisionpad.runs.create_instance import run_command

def attach_volume(boxname, volume_type, volume_size, env_vars, DB):

    region = env_vars['aws_region']
    access_key = env_vars['access_key']
    secret_key = env_vars['secret_key']
    awsf = AWSvolFuncs(region, access_key, secret_key)

    params = {}
    try:
        nametuple = DB['running_instances'][boxname]['sdrive_names'].pop(0)
        params['name'] = nametuple[0]
        params['mnt']  = nametuple[1]
    except:
        raise Exception('Maximum number of volumes you can attach reached')

    params['az']    = DB['running_instances'][boxname]['az']
    params['instance_id'] = DB['running_instances'][boxname]['id']
    params['size']  = volume_size
    params['vtype'] = volume_type

    params['vol_id'] = awsf.create_volume(params)

    DB['running_instances'][boxname]['sdrive'][params['name']] = params
    save_database(DB, env_vars['db_path'])

    print (' '.join(['ssh', boxname, 'sudo', 'mkfs', '-t', 'xfs', params['mnt']]))
    out = run_command(['ssh', boxname, 'sudo', 'mkfs', '-t', 'xfs', params['mnt']])
    drive_name = 'Project/{0}'.format(len(DB['running_instances'][boxname]['sdrive']))
    out = run_command(['ssh', boxname, 'sudo', 'mkdir', '-p', drive_name])
    out = run_command(['ssh', boxname, "echo 'sudo mount {0} ~/{1}' >> ~/.bashrc".format(params['mnt'], drive_name)])


