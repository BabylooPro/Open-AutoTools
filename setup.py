from setuptools import setup, find_packages

# READING REQUIREMENTS FROM FILE
with open('requirements.txt') as f:
    required = f.read().splitlines()

# SETUP CONFIGURATION FOR PACKAGE DISTRIBUTION
setup(
    name='Open-AutoTools',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        autocaps=autotools.cli:autocaps
        autocorrect=autotools.cli:autocorrect
    ''',
)
