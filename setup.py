import os
from setuptools import setup, find_packages

# READING README.MD FOR LONG DESCRIPTION
with open("README.md", "r", encoding="utf-8") as fh: long_description = fh.read()

# READING REQUIREMENTS FROM FILE
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    with open(requirements_path, "r", encoding="utf-8") as fh:
        requirements = []

        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                requirements.append(line)

        return requirements

required = read_requirements()

# SETUP CONFIGURATION FOR PACKAGE DISTRIBUTION
setup(
    name='Open-AutoTools',
    version='0.0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    
    # ENTRY POINTS FOR CLI COMMANDS
    entry_points='''
        [console_scripts]
        autotools=autotools.cli:cli
        autocaps=autotools.cli:autocaps
        autolower=autotools.cli:autolower
        autopassword=autotools.cli:autopassword
        autoip=autotools.cli:autoip
    ''',
    
    # METADATA FOR PYPI
    author="BabylooPro",
    author_email="maxremy.dev@gmail.com",
    description="A suite of automated tools accessible via CLI with a simple `autotools` command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BabylooPro/Open-AutoTools",
    project_urls={
        "Bug Tracker": "https://github.com/BabylooPro/Open-AutoTools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
