import os
import sys
from provisionpad.aws.aws_ec2 import AWSec2Funcs
# from provisionpad.helpers.namehelpers import vpc_name
from provisionpad.db.database import load_database, save_database

def create_vpc(env_vars, DB):
    # DB = load_database()
    region = env_vars['aws_region']
    access_key = env_vars['access_key']
    secret_key = env_vars['secret_key']
    awsf = AWSec2Funcs(region, access_key, secret_key)
    thename = env_vars['vpc_name']
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

# if __name__ == "__main__":
#     create_vpc()