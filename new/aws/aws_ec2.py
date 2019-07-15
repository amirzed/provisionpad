import os
import sys
repo_dir = os.environ['repo_home_dir']
sys.path.append(repo_dir)

import boto3
from collections import namedtuple



class AWSec2Funcs:

    def __init__(self, region, access_key, secret_key):
        self.region     = region
        self.access_key = access_key
        self.secret_key = secret_key 

        self.ec2 = boto3.resource('ec2', region_name=region,
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key )

        self.ec2Client = boto3.client('ec2', region_name=region,
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key )

       
    def create_vpc(self, thename):

        # create VPC
        vpc = self.ec2.create_vpc(CidrBlock='172.16.0.0/16')
        vpc.create_tags(Tags=[{'Key': 'Name', 'Value': thename}])
        vpc.wait_until_available()

        # enable public dns hostname so that we can SSH into it later
        self.ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
        self.ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )

        # create an internet gateway and attach it to VPC
        internetgateway = self.ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)

        # create a route table and a public route
        routetable = vpc.create_route_table()
        route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)

        # create subnet and associate it with route table
        subnet = self.ec2.create_subnet(CidrBlock='172.16.1.0/24', VpcId=vpc.id)
        routetable.associate_with_subnet(SubnetId=subnet.id)

        # Create a security group and allow SSH inbound rule through the VPC
        securitygroup = self.ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id)
        securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)

        vpctuple = namedtuple(thename, ['sg_id', 'subnet_id', 'vpc_id'])
        vpctuple.sg_id = securitygroup.id
        vpctuple.subnet_id = subnet.id
        vpctuple.vpc_id = vpc.id
 
        return vpctuple

