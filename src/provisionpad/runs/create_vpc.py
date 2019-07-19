import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
from aws.aws_ec2 import AWSec2Funcs
import redis
from helpers.namehelpers import vpc_name
from db.database import load_database, save_database

def create_vpc():
    DB = load_database()
    region = os.environ['aws_region']
    access_key = os.environ['aws_access_key_id']
    secret_key = os.environ['aws_secret_access_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)
    thename = vpc_name()
    if thename in DB:
        print ('The VPC with the name: {0} exists.'.format(thename))
        sys.exit()
    vpc_params = awsf.create_vpc(thename)
    print (vpc_params.sg_id, vpc_params.subnet_id, vpc_params.vpc_id)
    DB[thename] = {}
    DB[thename]['vpc_id']    = vpc_params.vpc_id
    DB[thename]['sg_id']     = vpc_params.sg_id
    DB[thename]['subnet_id'] = vpc_params.subnet_id
    save_database(DB)

if __name__ == "__main__":
    create_vpc()