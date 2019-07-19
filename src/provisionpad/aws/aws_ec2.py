import os
import sys
import time

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

        self.client = boto3.client('ec2', region_name=region,
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key )

       
    def create_vpc(self, thename):

        # create VPC
        vpc = self.ec2.create_vpc(CidrBlock='172.16.0.0/16')
        vpc.create_tags(Tags=[{'Key': 'Name', 'Value': thename}])
        vpc.wait_until_available()

        # enable public dns hostname so that we can SSH into it later
        self.client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
        self.client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )

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

    def get_instance_info(self,id, instances_info):
        rdict = {}
        for x in instances_info:
            for y in x['Instances']:
                if y['InstanceId']== id:
                    rdict['id'] = id
                    rdict['launch_time'] = y['LaunchTime']
                    rdict['type'] = y['InstanceType']
                    rdict['public_dns'] = y['PublicDnsName']
                    rdict['public_ip'] = y['PublicIpAddress']
                    rdict['private_dns'] = y['PrivateDnsName']
                    rdict['private_ip'] = y['PrivateIpAddress']
                    rdict['az'] = y['Placement']['AvailabilityZone'] # az is not me it is availabilityzone :D
                    rdict['pdrive'] = y['BlockDeviceMappings'][0]['Ebs']['VolumeId']
                    break
        return rdict

    def create_ec2_instance(self, params):

        instances = self.ec2.create_instances(
                        ImageId=params['aws_ami'],
                        InstanceType=params['box_type'],
                        MaxCount=1,
                        MinCount=1,
                        NetworkInterfaces=[{
                            'SubnetId': params['vpc']['subnet_id'],
                            'Groups': [params['vpc']['sg_id'],],
                            'DeviceIndex': 0,
                            'AssociatePublicIpAddress': True,
                        }],
                        TagSpecifications=[
                            {
                                'ResourceType': 'instance',
                                'Tags': [
                                    {
                                        'Key': 'Name',
                                        'Value': params['name']
                                    },
                                ]
                            },
                        ],
                        IamInstanceProfile={
                            # 'Arn': 'string',
                            'Name': params['aws_iam_role']
                        },
                        KeyName=params['ssh_key_name'])

        instances[0].wait_until_running()
        response = self.client.describe_instances()['Reservations']
        return self.get_instance_info(instances[0].id, response)

    def terminate_ec2_instance(self, id):
        ids = [id,]
        instances = self.ec2.instances.filter(InstanceIds=ids).terminate()
        # print (instances)
        # instances.wait_until_terminated()

    def stop_ec2_instance(self, id):
        ids = [id,]
        instances = self.ec2.instances.filter(InstanceIds=ids).stop()
        print (instances)
        # instances.wait_until_terminated()

    def start_ec2_instance(self, id):
        ids = [id,]
        instances = self.ec2.instances.filter(InstanceIds=ids).start()
        self.ec2.Instance(id=id).wait_until_running()
        response = self.client.describe_instances()['Reservations']
        return self.get_instance_info(id, response)

    def volume_waiter(self, id, state):
        # for i, x in enumerate(info):
        #     if x['VolumeId'] == id:
        #         index = i
        #         break
        tw = 0
        while True:
            if tw > 60:
                print ('it is taking too long to make this volume avaialable; volume waiter')
                sys.exit()
            info = self.client.describe_volumes()['Volumes']
            for x in info:
                if x['VolumeId'] == id:
                    if x['State'] == state:
                        return 
            time.sleep(5)
            tw += 5

    def create_volume(self, params):
        volume = self.ec2.create_volume(
            AvailabilityZone=params['az'],
            # Encrypted=True|False,
            # Iops=123,
            # KmsKeyId='string',
            Size=params['size'],
            # SnapshotId='string',
            VolumeType=params['vtype']   ,#'standard'|'io1'|'gp2'|'sc1'|'st1',
            TagSpecifications=[
                {
                    'ResourceType': 'volume',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': params['name']
                        },
                    ]
                },
            ]
        )
        self.volume_waiter(volume.id, 'available')
        response = volume.attach_to_instance(
            Device='/dev/xvdh',
            InstanceId=params['instance_id'],
            # DryRun=True|False
        )
        print (response)


        
    def get_volume_info(self, id):
        volume_info = self.client.describe_volumes()
        print (volume_info['Volumes'][0]['Attachments'])
        print (volume_info['Volumes'][1])
        print (len(volume_info['Volumes']) )