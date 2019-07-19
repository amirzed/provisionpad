import os
def vpc_name():
    return os.environ['your_name'].replace(" ", "")+'_VPC'