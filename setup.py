from setuptools import setup, find_packages
import os

# READING REQUIREMENTS FROM FILE
required = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as f:
        required = [line for line in f.read().splitlines() if "git+" not in line]

# SETUP CONFIGURATION FOR PACKAGE DISTRIBUTION
setup(
    name='Open-AutoTools',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        autotools=autotools.cli:autotools
        autocaps=autotools.cli:autocaps
        autolower=autotools.cli:autolower
        autodownload=autotools.cli:autodownload
        autopassword=autotools.cli:autopassword
        autotranslate=autotools.cli:autotranslate
        autoip=autotools.cli:autoip
    ''',
)
