
import sys
import os

from os.path import expanduser
home = expanduser("~")

def create_aliases():
    env_dir = os.path.join(home, '.provisionpad') 
    if not os.path.isdir(env_dir):
        os.mkdir(env_dir)
    if os.path.isfile(os.path.join(env_dir, 'aliases')):
        thein = input ('It seems you already have aliases'
                       'Do you want to replace it? (y/n): ')
        if thein.strip()=='y':
            os.remove(os.path.join(env_dir, 'aliases'))
        elif thein.strip() == 'n':
            return 
        else:
            print('Invalid input')
            sys.exit()

    rootpath = os.path.dirname(os.path.realpath(__file__))
    thebin = os.path.join(rootpath,'bin/ppad')

    with open(os.path.join(env_dir, 'aliases'), 'w') as f:
        f.write('alias ppad=\''+thebin+'\'')


create_aliases()

try:
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setup tools.", file=sys.stderr)
    sys.exit(1)


def read_requirements():
    rootpath = os.path.dirname(os.path.realpath(__file__))
    requirementPath = os.path.join(rootpath ,'requirements.txt')
    if os.path.isfile(requirementPath):
        with open(requirementPath) as f:
            install_requires = f.read().splitlines()
    return install_requires


static_setup_params = dict(
    name='provisionpad',
    version='0.0.0',
    description='Radically simple IT automation',
    author='AZ',
    author_email='amir.zainali@gmail.com',
    url='to add some url',
    project_urls={
        'Source Code': 'https://github.com/amirzed/provisionpad',
    },
    license='Apache-2.0',
    python_requires='>=2.7, >=3.7',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Development Status :: Test',
    ],
    scripts=[
        'bin/ppad',
    ],
)

def main():
    """Invoke installation process using setuptools."""
    setup_params = dict(static_setup_params, install_requires=read_requirements() )
    setup(**setup_params)

if __name__ == '__main__':
    main()

