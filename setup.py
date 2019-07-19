
import sys
try:
    from setuptools import setup, find_packages
    # from setuptools.command.build_py import build_py as BuildPy
    # from setuptools.command.install_lib import install_lib as InstallLib
    # from setuptools.command.install_scripts import install_scripts as InstallScripts
except ImportError:
    print("Please install setup tools.", file=sys.stderr)
    sys.exit(1)

import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
# setup(name="yourpackage", install_requires=install_requires, [...])

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
    setup_params = dict(static_setup_params, install_requires=install_requires)
    setup(**setup_params)

if __name__ == '__main__':
    main()

