import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
from pythonscripts.boxno import get_box_name
import redis

r = redis.Redis(
    host='localhost',
    port=6379, 
    password='')

def start_instance(boxname, boxtype):

    runnin_instances = r.smembers('running_instances')
    stopped_instances = r.smembers('stopped_instances')

    my_ssh_key_path = os.environ['my_ssh_key']
    ssh_key_name = my_ssh_key_path.strip().rsplit('/', 1)[-1].split('.')[0]
    os.environ["keypair"] = ssh_key_name
    # os.environ["instance_type"] = box_type
    if not boxname:
        boxname = get_box_name('available_names', 'created_instances')
    else:
        if boxname[:3] == 'box' or \
           boxname.encode('utf-8') in runnin_instances or \
           boxname.encode('utf-8') in stopped_instances:
            print ("enter a better name. either exists or starts with box")
            sys.exit()

    os.environ['boxname'] = boxname
    os.environ['boxtype'] = boxtype
    ansible_file = os.path.join(repo_dir,'playbooks/start_ec2.yml')
    
    os.system(' '.join(['ansible-playbook', ansible_file]))


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


    start_instance(boxname, boxtype)

