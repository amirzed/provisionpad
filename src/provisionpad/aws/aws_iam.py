import os
import sys
import boto3
from botocore.exceptions import ClientError
import json
import time
from provisionpad.aws.aws_sts import AWSstsFuncs

class AWSiamFuncs:

    def __init__(self, region, access_key, secret_key):
        self.region     = region
        self.access_key = access_key
        self.secret_key = secret_key 

        self.client = boto3.client('iam', region_name=region,
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key )

        self.iam = boto3.resource('iam', region_name=region,
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key )

        self.sts = AWSstsFuncs(region, access_key, secret_key)

    def ec2_policy_access_full(self, policy_name):
        account_id = self.sts.get_account_id()
        policy_arn = 'arn:aws:iam::{0}:policy/{1}'.format(account_id, policy_name)
        if self.check_policy_exists(policy_arn):
            return policy_arn
        else:
            policy_doc = {
                            "Version": "2012-10-17",
                            "Statement": [{"Effect": "Allow",
                                        "Action": "s3:*",
                                        "Resource": "*"
                                        }
                            ]
            }
            self.client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_doc),
                Description='grant full access to s3'
            )
            if not self.check_policy_exists(policy_arn, delay=2, maxattempts=3):
                raise Exception('It seems it was not able to create the policy check your AWS permissions')
            return policy_arn

    def check_policy_exists(self, policy_arn, delay=1, maxattempts=1):
        waiter = self.client.get_waiter('policy_exists')
        try:
            waiter.wait(
                PolicyArn=policy_arn,
                WaiterConfig={
                    'Delay': delay,
                    'MaxAttempts': maxattempts
                }
            )
        except: 
            return False
        return True

    def create_role_for_ec2(self, role_name):  
        account_id = self.sts.get_account_id()
        role_arn = 'arn:aws:iam::{0}:role/{1}'.format(account_id, role_name)
        base_policy = { "Version": "2012-10-17", 
                        "Statement": [ { "Effect": "Allow", 
                                         "Principal": { "Service": "ec2.amazonaws.com" }, 
                                         "Action": "sts:AssumeRole" } ] }  
        response = self.client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(base_policy),
            Description='ec2_policy',
        )
        return role_arn

    def attach_policy_to_role(self, role_name, policy_arn):
        role = self.iam.Role(role_name)
        response = role.attach_policy(PolicyArn=policy_arn)

    def check_role_exists(self, role_name, delay=1, maxattempts=1):
        try:
            waiter = self.client.get_waiter('role_exists')
            waiter.wait(
                RoleName=role_name,
                WaiterConfig={
                    'Delay': delay,
                    'MaxAttempts': maxattempts
                }
            )
        except:
            return False
        return True

    def create_instance_profile(self, name):
        instance_profile = self.iam.create_instance_profile(
            InstanceProfileName=name,
        )
        time.sleep(1)
        instance_profile.add_role(
            RoleName=name
        )



