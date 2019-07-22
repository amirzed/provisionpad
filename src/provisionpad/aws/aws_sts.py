import boto3

class AWSstsFuncs:

    def __init__(self, region, access_key, secret_key):

        self.client = boto3.client('sts', region_name=region,
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key )

    def get_account_id(self):
        return self.client.get_caller_identity()["Account"]