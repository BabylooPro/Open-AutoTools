from setuptools import setup, find_packages
import os

# READING README.MD FOR LONG DESCRIPTION
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# FIX: READING REQUIREMENTS FROM FILE IN RELEASED VERSION, CAN BUILD WITHOUT LISTED REQUIREMENTS HERE
# READING REQUIREMENTS
required = [
    "Brotli==1.1.0",
    "certifi==2024.2.2",
    "charset-normalizer==3.3.2",
    "click==8.1.3",
    "cryptography==42.0.2",
    "idna==3.6",
    "importlib-metadata>=7.0.1",
    "packaging>=23.0",
    "platformdirs==4.2.0",
    "pycryptodomex==3.20.0",
    "pyperclip==1.8.2",
    "python-dotenv>=1.0.0",
    "requests>=2.32.2",
    "tomli==2.0.1",
    "tqdm==4.66.2",
    "urllib3==2.2.1",
    "websockets==13.0.1",
    "yapf==0.40.2",
    "zipp==3.17.0",
    "netifaces>=0.11.0",
    "speedtest-cli>=2.1.3",
    "psutil>=5.9.0",
    "setuptools>=40.8.0",
    "halo>=0.0.31",
]

# SETUP CONFIGURATION FOR PACKAGE DISTRIBUTION
setup(
    name='Open-AutoTools',
    version='0.0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    
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

    # ENTRY POINTS FOR CLI COMMANDS
    entry_points='''
        [console_scripts]
        autotools=autotools.cli:cli
        autocaps=autotools.cli:autocaps
        autolower=autotools.cli:autolower
        autopassword=autotools.cli:autopassword
        autoip=autotools.cli:autoip
    ''',
    
    # TEST REQUIREMENTS
    extras_require={
        'test': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pytest-sugar>=1.0.0',
            'pytest-xdist>=3.5.0',
            'pytest-timeout>=2.2.0',
        ],
    },
)
