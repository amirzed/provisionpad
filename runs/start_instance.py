import os

def start_instance(box_name, box_type):
    my_ssh_key_path = os.environ['my_ssh_key']
    ssh_key_name = my_ssh_key_path.strip().rsplit('/', 1)[-1].split('.')[0]


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='A function to create instance', 
                                     usage='%(prog)s [OPTIONS]')
    parser.add_argument("-n", "--name", dest="boxname", default="", 
                        help="Enter the name of the sandbox:")
    parser.add_argument("-t", "--type", dest="boxtype", default="", 
                        help="The type of instance. For example for ec2 t2.micro blah blah")
    args = parser.parse_args()
    
    box_name = args.boxname
    box_type = args.boxtype

    start_instance(box_name, box_type)

