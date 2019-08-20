
import sys
import os

from os.path import expanduser
home = expanduser("~")

try:
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setup tools.")
    sys.exit(1)

def read_file(file_name):
    '''
    Read a file and return stringls
    '''
    with open(file_name, 'r') as f:
        return f.read()

setup (
    name='provisionpad',
    version='0.0.3',
    description='The easiest way to create and connect to secure cloud instances',
    long_description=read_file('README.md'),
    author='Amir Zainali',
    author_email='provisionpad@gmail.com',
    url='https://www.provisionpad.com/',
    install_requires=['boto3',
                      'python-dateutil',
                      'future',
                      'argcomplete',
                      'colorclass',
                      'terminaltables',
                      'tzlocal',
                      'requests'],
    project_urls={
        'Source Code': 'https://github.com/provisionpad/provisionpad',
    },
    license='Apache-2.0',
    # python_requires='>=2.7, >=3.7',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'propad = provisionpad.bin.propad:main',
        ]
    }
)


