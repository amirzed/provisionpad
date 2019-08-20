from provisionpad.aws.aws_ec2 import AWSec2Funcs
from requests import get
from provisionpad.db.database import load_database, save_database


class AWSsgFuncs(AWSec2Funcs):

    @staticmethod
    def get_ip_address():
        '''
        Returns:
            Public IP address of the machine
        '''
        return get('https://api.ipify.org').text

    def check_public_ip(self, env_vars, DB):
        thepublicip = AWSsgFuncs.get_ip_address()
        if thepublicip != DB['public_ip']:
            print ('Your public_ip has changed from {0} to {1}'.format(DB['public_ip'], thepublicip))
            DB['public_ip'] = thepublicip
        save_database(DB, env_vars['db_path'])

    def set_sg_sshonly_local_ip(self, sgid, publicip):
        '''
        modifies the security group to only ssh ingress and
        no egress

        Parameters:
            sgid (str): the id of the security group

        Returns:
            -
        '''
        # ip = AWSsgFuncs.get_ip_address()
        myipaddress = '{0}/32'.format(publicip)
        securitygroup = self.ec2.SecurityGroup(sgid)
        # using json request format like set_sg_http_egress
        # was producing strange errors. Just used the following format --Amir
        securitygroup.authorize_ingress(CidrIp=myipaddress,
                                        IpProtocol='tcp',
                                        FromPort=22,
                                        ToPort=22)



    def set_sg_http_egress(self, sgid):
        '''
        modifies the security group to only ssh ingress and
        no egress

        Parameters:
            sgid (str): the id of the security group

        Returns:
            -
        '''
        securitygroup = self.ec2.SecurityGroup(sgid)
        securitygroup.authorize_egress(
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges':   [{'CidrIp': '0.0.0.0/0'}],
                'Ipv6Ranges': [{'CidrIpv6': '::/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'IpRanges':   [{'CidrIp': '0.0.0.0/0'}],
                'Ipv6Ranges': [{'CidrIpv6': '::/0'}]},
            ]
        )


    def revoke_sg_permissions_all(self,vpcid):
        '''
        revokes all the egress and ingress security permissions

        Parameters:
            vpcid (str): the id of vpc to revoke permissions

        Returns:
            -
        '''
        clientsecgrps = self.client.describe_security_groups(Filters=[ { 'Name': 'vpc-id', 'Values': [vpcid] }])
        groups = clientsecgrps['SecurityGroups']

        for group in groups:
            if len(group['IpPermissions']) > 0:
                for permission in group['IpPermissions']:
                    self.client.revoke_security_group_ingress(GroupId=group['GroupId'],IpPermissions=[permission])
            if len(group['IpPermissionsEgress']) > 0:
                for permission in group['IpPermissionsEgress']:
                    self.client.revoke_security_group_egress(GroupId=group['GroupId'],IpPermissions=[permission])