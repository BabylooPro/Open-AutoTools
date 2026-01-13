import os
import importlib.util
from setuptools import setup, find_packages

# READING README.MD FOR LONG DESCRIPTION
with open("README.md", "r", encoding="utf-8") as fh: long_description = fh.read()

# LOADING REQUIREMENTS
requirements_module_path = os.path.join(os.path.dirname(__file__), "autotools", "utils", "requirements.py")
spec = importlib.util.spec_from_file_location("requirements", requirements_module_path)
requirements_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(requirements_module)
read_requirements = requirements_module.read_requirements

required = read_requirements("requirements.txt")
dev_required = read_requirements("requirements-dev.txt")

# SETUP CONFIGURATION FOR PACKAGE DISTRIBUTION
setup(
    name='Open-AutoTools',
    version='0.0.4',
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=required,
    extras_require={ "dev": dev_required },
    
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
    project_urls={ "Bug Tracker": "https://github.com/BabylooPro/Open-AutoTools/issues" },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
