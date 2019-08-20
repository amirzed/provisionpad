import sys
import time
from provisionpad.aws.aws_ec2 import AWSec2Funcs

class AWSvolFuncs(AWSec2Funcs):

    def volume_waiter(self, id, state):
        tw = 0
        while True:
            if tw > 120:
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
            Size=params['size'],
            VolumeType=params['vtype']   , #'standard'|'io1'|'gp2'|'sc1'|'st1',
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
        volume.attach_to_instance(
            Device=params['mnt'],
            InstanceId=params['instance_id'],
        )
        time.sleep(2)
        return volume.id

    def get_volume_info(self, id):
        volume_info = self.client.describe_volumes()
        print (volume_info['Volumes'][0]['Attachments'])
        print (volume_info['Volumes'][1])
        print (len(volume_info['Volumes']) )

    def delete_vol(self, id):
        self.client.detach_volume(
            VolumeId=id,
            Force=True
        )
        self.volume_waiter(id, 'available')
        self.client.delete_volume(
            VolumeId=id
        )