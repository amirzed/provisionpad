import re
import os
import sys

def create_dir_for_file(filepath):
    thedir = os.path.dirname(os.path.realpath(filepath))
    if not os.path.isdir(thedir):
        os.makedirs(thedir)
        print('dir did not exist created one')

def write_into_text(marker, text, filetowrite):
    create_dir_for_file(filetowrite)
    pattern = '### PROVISIONPAD {0}\n.*?\n### PROVISIONPAD'.format(marker)
    if not os.path.isfile(filetowrite):
        with open(filetowrite, 'w+') as f:
            f.write(
            '### PROVISIONPAD {0}\n{1}\n### PROVISIONPAD\n'.format(
                marker, text.strip())
            )
    else:
        with open(filetowrite, 'r') as f:
            textfile = f.read()
        with open(filetowrite, 'a+') as f:
            f.write(
            '\n### PROVISIONPAD {0}\n{1}\n### PROVISIONPAD\n'.format(
                marker, text.strip())
            )            

def delete_text_from_file(marker, filetodelete):
    create_dir_for_file(filetodelete)
    pattern = '### PROVISIONPAD {0}\n.*?\n### PROVISIONPAD'.format(marker)
    if not os.path.isfile(filetodelete):
        print ('the file does not exists. Will ignore it for now') 
    else:
        with open(filetodelete, 'r') as f:
            textfile = f.read()
            modified_text = re.sub(pattern, '', textfile, flags=re.DOTALL)
        with open(filetodelete, 'w') as f:
            f.write(modified_text)

def clean_propad_from_file(filetodelete):
    create_dir_for_file(filetodelete)
    pattern = '### PROVISIONPAD.*?\n### PROVISIONPAD'
    if not os.path.isfile(filetodelete):
        pass
    else:
        with open(filetodelete, 'r') as f:
            textfile = f.read()
            modified_text = re.sub(pattern, '', textfile, flags=re.DOTALL)
            texttowrite = ''
            for line in modified_text.split('\n'):
                if line != '':
                    texttowrite += line+'\n'

        with open(filetodelete, 'w') as f:
            f.write(texttowrite)
                 

