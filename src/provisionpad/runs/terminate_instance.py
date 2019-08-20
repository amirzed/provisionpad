import os
import sys
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from provisionpad.aws.aws_vol import AWSvolFuncs
from provisionpad.db.database import load_database, save_database
from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.helpers.texthelpers import delete_text_from_file
from provisionpad.runs.create_instance import run_command
import textwrap


def terminate_instance(boxname, env_vars, DB):

    if boxname in DB['stopped_instances']:
        raise ValueError(textwrap.dedent('''\
              Instance {name} is in stopped state and can not be terminated
                          To terminate the instance you need to first start it:
                          propad start {name}; then you can stop it
        '''.format(name=boxname)))

    region = env_vars['aws_region']
    home_folder = env_vars['HOME']
    access_key = env_vars['access_key']
    secret_key = env_vars['secret_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)
    awsvolf = AWSvolFuncs(region, access_key, secret_key)
    for _, val in DB['running_instances'][boxname]['sdrive'].items():
        id = val['vol_id']
        print (val['vol_id'], val['name'])
        out = run_command(['ssh', boxname, 'umount', val['mnt']])
        awsvolf.delete_vol(id)


    id = DB['running_instances'][boxname]['id']
    awsf.terminate_ec2_instance(id)
    del(DB['running_instances'][boxname])
    if boxname[0:3] == 'box':
        DB['available_names'].append(boxname)
    save_database(DB, env_vars['db_path'])
    delete_text_from_file(boxname, os.path.join(home_folder,'.ssh/config'))



    print ('ec2 instance {0} terminated successfully'.format(boxname))
