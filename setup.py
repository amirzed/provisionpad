
import sys
import os

from os.path import expanduser
home = expanduser("~")

try:
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setup tools.")
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

