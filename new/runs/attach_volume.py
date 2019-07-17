import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
from aws.aws_ec2 import AWSec2Funcs
from db.database import load_database, save_database
from helpers.namehelpers import vpc_name
from helpers.texthelpers import write_into_text

def create_volume(box_name, volume_name, volume_type, volume_size,  DB):

    # if boxname not in DB['stopped_instances']:
    #     print ('the box is not available check again:')
    #     sys.exit()

    region = os.environ['aws_region']
    home_folder = os.environ['my_home_folder']
    access_key = os.environ['aws_access_key_id']
    secret_key = os.environ['aws_secret_access_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)

    params = {}
    params['az']    = DB['running_instances'][box_name]['az']
    params['size']  = volume_size
    params['vtype'] = volume_type
    params['name']  = volume_name

    # awsf.create_volume(params) 
    awsf.get_volume_info('ddd')


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='A function to create instance', 
                                     usage='%(prog)s [OPTIONS]')
    parser.add_argument("-b", "--box_name", dest="box_name", default="", 
                        help="Enter the name of the sandbox:")
    parser.add_argument("-n", "--volume_name", dest="volume_name", default="", 
                        help="Enter the name of volume:")
    parser.add_argument("-s", "--volume_size", dest="volume_size", default="", 
                        help="Enter the volume size:")
    parser.add_argument("-t", "--volume_type", dest="volume_type", default="gp2", 
                        help="Enter the volume size:")
    args = parser.parse_args()
    
    box_name = args.box_name
    volume_name = args.volume_name
    volume_size = int(args.volume_size)
    volume_type = args.volume_type

    if not box_name:
        print('Please enter the name of the box you want to remove')
        sys.exit()
    if not volume_name:
        volume_name = box_name+'VOL'
    if not volume_size:
        print('Please enter the size of the volume')
        sys.exit()

    DB = load_database()
    create_volume(box_name, volume_name, volume_type, volume_size,  DB)