import re
import os
import sys

def create_dir_for_file(filepath):
    thedir = filepath.strip().rsplit('/',1)[0]
    if not os.path.isdir(thedir):
        os.makedirs(thedir)
        print('dir did not exist created one')

def write_into_text(marker, text, filetowrite):
    create_dir_for_file(filetowrite)
    pattern = '### PROVISIONPAD {0}\n.*?\n### PROVISIONPAD {0}'.format(marker)
    if not os.path.isfile(filetowrite):
        with open(filetowrite, 'w+') as f:
            f.write(
            '### PROVISIONPAD {0}\n{1}\n### PROVISIONPAD {0}\n'.format(
                marker, text.strip())
            )
    else:
        with open(filetowrite, 'r') as f:
            textfile = f.read()
        with open(filetowrite, 'a+') as f:
            if len(re.findall(pattern, textfile, flags=re.DOTALL))>0:
                print('something wrong fix it (write_into_text)')
                sys.exit()
            f.write(
            '\n### PROVISIONPAD {0}\n{1}\n### PROVISIONPAD {0}\n'.format(
                marker, text.strip())
            )            

def delete_text_from_file(marker, filetodelete):
    create_dir_for_file(filetodelete)
    pattern = '### PROVISIONPAD {0}\n.*?\n### PROVISIONPAD {0}'.format(marker)
    if not os.path.isfile(filetodelete):
        print ('the file does not exists')
        sys.exit()
    else:
        with open(filetodelete, 'r') as f:
            textfile = f.read()
            if len(re.findall(pattern, textfile, flags=re.DOTALL)) != 1:
                print ('something is wrong check it')
                sys.exit()
            modified_text = re.sub(pattern, '', textfile, flags=re.DOTALL)
        with open(filetodelete, 'w') as f:
            f.write(modified_text)
                 

# # write_into_text('test1', 
# # '''
# # amir davala
# # mire be bazar
# #  ssdfsdf
# # ''', '/tmp/amirtest')

# delete_text_from_file('daval', '/tmp/amirtest')




# a = r''' 
# Example
# ### Amir This is a very annoying string
# that takes up multiple lines
# bbb
# and h@s a// kind{s} of stupid symbols in it
# ### Amir ok String'''

# # with open('text.in', 'r') as f:
# #     a = f.read()

# # c = re.sub('\n### Amir.*?### Amir','',a, flags=re.DOTALL)
# c = re.findall('\n### Amir.*?### Amir', a, flags=re.DOTALL)

# print (c)

# # with open('/tmp/text.test', 'a') as f:
# #     f.write('dd')

# # os.path.isfile()
# # import os

# # def create_dir_for_file(filepath):
# #     thedir = filepath.strip().rsplit('/',1)[0]
# #     if not os.path.isdir(thedir):
# #         os.makedirs(thedir)
# #         print('dir did not exist created one')

# # def append_text_to_file

# # textfile = '/home/sandbox/ddsd/bbb/test.txt'

# # create_dir_for_file(textfile)
