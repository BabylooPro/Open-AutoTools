from setuptools import setup, find_packages

# READING REQUIREMENTS FROM FILE
with open('requirements.txt') as f:
    required = [line for line in f.read().splitlines() if "git+" not in line] # ignore git+ links in requirements if "pip freeze > requirements.txt" generates them

# SETUP CONFIGURATION FOR PACKAGE DISTRIBUTION
setup(
    name='Open-AutoTools',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        autotools=autotools.cli:autotools
        autocaps=autotools.cli:autocaps
        autocorrect=autotools.cli:autocorrect
        autotranslate=autotools.cli:autotranslate
        autodownload=autotools.cli:autodownload
    ''',
)
