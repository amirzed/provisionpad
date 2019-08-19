import sys
import os
import argparse
import argcomplete
import json
import textwrap
from provisionpad.db.database import load_database
from provisionpad.runs.create_instance import create_instance
from provisionpad.runs.terminate_instance import terminate_instance
from provisionpad.runs.stop_instance import stop_instance
from provisionpad.runs.start_instance import start_instance
from provisionpad.runs.create_vpc import create_vpc
from provisionpad.runs.initiate import initiate
from provisionpad.runs.status import show_status
from provisionpad.runs.attach_volume import attach_volume
from provisionpad.aws.aws_sg import AWSsgFuncs

shut_down_time = 50

from argparse import RawTextHelpFormatter

class PPAD(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='A very simple command line tool to control'
                        'your remote cloud based workstation',
            usage='''%(prog)s <command> [<args>]

The following commands are available:
    initiate   :   Initiate your test environment; only use it once
    create     :   Create a new computing instance
    terminate  :   Terminate the already running instance
    stop       :   Stop the running instance
    start      :   Start an stopped instance
    stat       :   Get the information on the current workspace
    allowhttp  :   Opens http(s) egress permission for security group
    resolvesg  :   Back to default security group
''')
        parser.add_argument('command', help='Choose one of (initiate, create, terminate, stop, start, stat) to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print ('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    @staticmethod
    def get_env_vars():
        home = os.path.expanduser("~")
        env_dir = os.path.join(home, '.provisionpad')
        env_var_path = os.path.join(env_dir, 'env_variable.json')
        with open(env_var_path, 'r') as f:
            env_vars = json.load(f)
            if env_vars['env_path'] != env_var_path:
                print ('something wrong')
                raise ('The environment variable seems to be a wrong one')
        env_vars = {str(key):str(val) for key, val in env_vars.items()}
        return env_vars

    def initiate(self):
        initiate()

    def create(self):

        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])

        parser = argparse.ArgumentParser(
            description='Create a new computing instance',
            usage='''propad create [option]s

If no name is provided an automatic name starting with box will be used.
Please note you can not use names starting with box.
If no instance type is provided the default t2.micro will be sued for aws
as the instance type qualifies for the free tier

''')

        parser.add_argument('name', nargs='?', help='Enter the name you want to use')
        parser.add_argument('-t', '--type', dest='type', type=str, default='t2.micro', help='''Enter the type of computing instance
                                                    If you are using AWS see the following link for further info:
                                                    https://aws.amazon.com/ec2/pricing/on-demand/
                                                    ''')

        args = parser.parse_args(sys.argv[2:])

        if not args.name:
            boxname = ''
        else:
            boxname = args.name

        boxtype = args.type

        create_instance(boxname, boxtype, shut_down_time, env_vars, DB)

    def terminate(self):

        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])

        parser = argparse.ArgumentParser(
            description='Create a new computing instance',
            usage='''propad terminate thename

for example:
    propad terminate box2
    the command above will terminate the box2 and the associated root volume

''')

        parser.add_argument('name', nargs='?', help='Enter the name of the box you want to terminate')

        args = parser.parse_args(sys.argv[2:])
        boxname = args.name
        if not boxname:
            raise NameError('You need to enter the name of the box')
        terminate_instance(boxname, env_vars, DB)

    def stop(self):

        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])

        parser = argparse.ArgumentParser(
            description='Create a new computing instance',
            usage='''propad stop thename

for example:
    propad top box2
    the command above will stop the box2 and the associated root volume

''')

        parser.add_argument('name', nargs='?', help='Enter the name of the box you want to terminate')

        args = parser.parse_args(sys.argv[2:])

        boxname = args.name
        if not boxname:
            raise NameError('You need to enter the name of the box')

        stop_instance(boxname, env_vars, DB)

    def start(self):

        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])

        parser = argparse.ArgumentParser(
            description='Create a new computing instance',
            usage='''propad stop [instancename]

for example:
    propad start box2
    the command above will restart the stopped box2

''')

        parser.add_argument('name', nargs='?', help='Enter the name of the box you want to terminate')

        args = parser.parse_args(sys.argv[2:])

        boxname = args.name
        if not boxname:
            raise NameError('You need to enter the name of the box')

        start_instance(boxname, env_vars, DB)


    def stat(self):
        '''
        Prints out the stat of the running and stopped instances
        '''

        self.resolvesg()
        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])
        show_status(env_vars, DB)

    def allowhttp(self):
        '''
        allow http access for the given box name
        '''

        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])

        region = env_vars['aws_region']
        access_key = env_vars['access_key']
        secret_key = env_vars['secret_key']

        awssgf = AWSsgFuncs(region, access_key, secret_key)
        awssgf.check_public_ip(env_vars, DB)
        vpcparams = DB[env_vars['vpc_name'] ]
        awssgf.revoke_sg_permissions_all(vpcparams['vpc_id'])
        awssgf.set_sg_sshonly_local_ip(vpcparams['sg_id'], DB['public_ip'])
        awssgf.set_sg_http_egress(vpcparams['sg_id'])

    def resolvesg(self):
        '''
        limit the access to ssh-only from local machine.
        If you change your location then you need to update this function
        '''

        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])

        region = env_vars['aws_region']
        access_key = env_vars['access_key']
        secret_key = env_vars['secret_key']

        awssgf = AWSsgFuncs(region, access_key, secret_key)
        awssgf.check_public_ip(env_vars, DB)
        vpcparams = DB[env_vars['vpc_name'] ]
        awssgf.revoke_sg_permissions_all(vpcparams['vpc_id'])
        awssgf.set_sg_sshonly_local_ip(vpcparams['sg_id'], DB['public_ip'])

    def vol(self):
        '''
        attach volume to instance
        '''

        env_vars = PPAD.get_env_vars()
        DB = load_database(env_vars['db_path'])

        parser = argparse.ArgumentParser(
            description='Attach a volume to running instance',
            usage='''propad vol [instancename]

for example:
    propad vol box2 -s 10 -t g2

''')

        parser.add_argument('name', nargs='?', help='Enter the name of the box you want to terminate')
        parser.add_argument("-s", "--volsize", type=int, dest="volumesize",
                            help="Enter the volume size:")
        parser.add_argument("-t", "--voltype", dest="volumetype", default="gp2",
                            help="Enter the volume type")
        args = parser.parse_args(sys.argv[2:])

        boxname = args.name
        if not boxname:
            raise NameError('You need to enter the name of the box')
        elif boxname not in DB['running_instances']:
            raise ValueError('You can only attach a volume to running instance')

        volsize = args.volumesize
        if not volsize:
            raise ValueError('You need to provide the volume size')

        voltype = args.volumetype

        attach_volume(boxname, voltype, volsize, env_vars, DB)

def main():
   PPAD()

if __name__ == '__main__':
    main()

