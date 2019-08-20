import platform
import sys
import re
import os
import json
import subprocess
import boto3
import textwrap
from builtins import input
from provisionpad.aws.aws_ec2 import AWSec2Funcs
from  provisionpad.aws.aws_sg import AWSsgFuncs
from provisionpad.aws.aws_iam import AWSiamFuncs
from provisionpad.aws.aws_sts import AWSstsFuncs
from provisionpad.db.database import load_database, save_database
from provisionpad.runs.create_vpc import create_vpc

def initiate():

    home = os.path.expanduser("~")
    env_dir = os.path.join(home, '.provisionpad')
    if not os.path.isdir(env_dir):
        os.mkdir(env_dir)
    dbpath = os.path.join(env_dir, 'database.p')
    DB = load_database(dbpath)

    home = os.path.expanduser("~")
    env_dir = os.path.join(home, '.provisionpad')
    if not os.path.isdir(env_dir):
        os.mkdir(env_dir)

    env_var_path = os.path.join(env_dir, 'env_variable.json')
    input_var_path = os.path.join(env_dir, 'input_variable.json')


    if not os.path.isfile(input_var_path):
        env_vars = {}
        ask_for_credentials = True
        print ('Initiating a new propad environment')
        print ('Searching for default AWS credentials...')
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            use_default_cred = input(textwrap.dedent('''\
                                        Default AWS credentials found.
                                        Do you want to use them?(y/n)
                                        '''))
            if str(use_default_cred).strip()[0] == 'y':
                env_vars['access_key'] = credentials.access_key
                env_vars['secret_key'] = credentials.secret_key
                ask_for_credentials = False
        if ask_for_credentials:
            print ('  You can find aws access keys under user tab (top third from right)')
            print ('  My security credentials for the root info or under IAM users section')
            print ('  For more information please visit: https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html')
            access_key = input('Enter AWS access key ID: ')
            env_vars['access_key'] = str(access_key).strip()
            if not env_vars['access_key']:
                print ('Invalid input')
                sys.exit()
            secret_key = input('Enter AWS secret access key: ')
            env_vars['secret_key'] = str(secret_key).strip()
            if not env_vars['secret_key']:
                print ('Invalid input')
                sys.exit()
        your_name  = input('Enter your name (optional, will be added as a tag to the instance): ')
        env_vars['your_name'] = re.sub('[^a-zA-Z0-9]', '', your_name).upper()
        if not env_vars['your_name']:
            print ('Invalid input')
            sys.exit()
        # env_vars['your_email'] = input('Enter your email (): ')
        print ('\n')
        print ('Note: AMI (Image) should be in the same defined AWS region.')
        env_vars['aws_region'] = input ('Enter AWS region (us-east-2): ')
        if not env_vars['aws_region']:
            env_vars['aws_region'] = 'us-east-2'
        env_vars['aws_ami'] = input ('Enter your AWS AMI. (Ubuntu 18): ')
        if not env_vars['aws_ami']:
            env_vars['aws_ami'] = 'ami-029f8374ffdc9a057'  #'ami-00df714b389c23925'

        with open(input_var_path, 'w') as f:
            json.dump(env_vars, f, indent=4)

    else:

        with open(input_var_path, 'r') as f:
            env_vars = json.load(f)

    env_vars['db_path'] = dbpath
    env_vars['env_path'] = env_var_path
    env_vars['env_dir'] = env_dir

    key_pair_name = 'ec2_keypair_{0}_{1}.pem'.format(env_vars['your_name'], env_vars['aws_region'])
    key_pair_path = os.path.join(env_dir, key_pair_name)

    env_vars['key_pair_name'] = key_pair_name
    env_vars['key_pair_path'] = key_pair_path

    env_vars['vpc_name'] = '{0}_VPC'.format(env_vars['your_name'])

    role_name   = [env_vars['your_name'] ]
    policies = ['S3FULL']
    role_name.extend(policies)
    role_names = ''.join(role_name)

    env_vars['policy'] = policies
    env_vars['role_name'] = role_names

    env_vars['HOME'] = home

    # get the public ip address of local machine
    DB['public_ip'] = AWSsgFuncs.get_ip_address()
    save_database(DB, env_vars['db_path'])

    create_vpc(env_vars, DB)

    awsec2f = AWSec2Funcs(env_vars['aws_region'], env_vars['access_key'], env_vars['secret_key'])
    awsstsf = AWSstsFuncs(env_vars['aws_region'], env_vars['access_key'], env_vars['secret_key'])
    awsiamf = AWSiamFuncs(env_vars['aws_region'], env_vars['access_key'], env_vars['secret_key'])

    if not os.path.isfile(env_vars['key_pair_path']):
        if not awsec2f.check_key_pair(env_vars['key_pair_name']):
            try:
                print ('creating key pair')
                with open(env_vars['key_pair_path'], 'w') as f:
                    key_pair = str(awsec2f.create_key_pair(key_pair_name))
                    print (key_pair)
                    f.write(key_pair)
                os.chmod(env_vars['key_pair_path'], 0o600)
            except:
                os.remove(env_vars['key_pair_path'])
                raise Exception('You do not have access to create key-pair check your permissions')
        else:
            raise Exception('we can find the public key but pem is not available')
    else:
        print ('the key pair exists')

    account_id = awsstsf.get_account_id()
    policy_attach = []
    for policy in env_vars['policy']:
        policy_arn = 'arn:aws:iam::{0}:policy/{1}'.format(account_id, policy )
        if not awsiamf.check_policy_exists(policy_arn):
            if policy == 'S3FULL':
                awsiamf.ec2_policy_access_full(policy)
                policy_attach.append(policy_arn)
            else:
                print ('the policy {0} not implemented yet'.format(policy))
        else:
            print ('the policy {0} exists'.format(policy))
            policy_attach.append(policy_arn)

    if not awsiamf.check_role_exists(env_vars['role_name']):
        print (awsiamf.create_role_for_ec2(env_vars['role_name']) )
        awsiamf.create_instance_profile(env_vars['role_name'])

    if awsiamf.check_role_exists(env_vars['role_name'], 1, 5):
        for policy in policy_attach:
            print ('attaching policy arn: {0}'.format(policy))
            awsiamf.attach_policy_to_role(env_vars['role_name'], policy)
            print ('policy attached')
    else:
        raise Exception(' was not able to find the role')


    with open(env_var_path, 'w') as f:
        json.dump(env_vars, f, indent=4)