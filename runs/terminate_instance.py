import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
import redis
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)

r = redis.Redis(
    host='localhost',
    port=6379, 
    password='')

def terminate_instance(instance_name):
    os.environ['instance_name'] = instance_name
    ansible_file = os.path.join(repo_dir,'playbooks/terminate_ec2.yml')    
    os.system(' '.join(['ansible-playbook', ansible_file]))
    r.srem('running_instances', instance_name)
    if instance_name[:3] == 'box':
        r.rpush('available_names', instance_name)
    r.delete(instance_name)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='A function to terminate instance', 
                                     usage='%(prog)s [OPTIONS]')
    parser.add_argument("-n", "--name", dest="instance_name", default="", 
                        help="Enter the name of the sandbox to stop")
    args = parser.parse_args()
    
    instance_name = args.instance_name
    if not instance_name:
        print ('Please enter the name of the instance you want to remove. For the list of running instances enter ...')
        sys.exit()

    terminate_instance(instance_name)