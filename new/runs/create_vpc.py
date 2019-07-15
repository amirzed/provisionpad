import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)
from aws.aws_ec2 import AWSec2Funcs
import redis
from helpers.namehelpers import vpc_name

r = redis.Redis(
    host='localhost',
    port=6379, 
    password='')


def create_vpc():
    region = os.environ['aws_region']
    access_key = os.environ['aws_access_key_id']
    secret_key = os.environ['aws_secret_access_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)
    thename = vpc_name()
    if r.exists(thename):
        print ('The VPC with the name: {0} exists.'.format(thename))
        sys.exit()
    vpc_params = awsf.create_vpc(thename)
    print (vpc_params.sg_id, vpc_params.subnet_id, vpc_params.vpc_id)
    r.rpush(thename, vpc_params.vpc_id)
    r.rpush(thename, vpc_params.sg_id)
    r.rpush(thename, vpc_params.subnet_id)

if __name__ == "__main__":
    create_vpc()