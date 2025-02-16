from setuptools import setup, find_packages
import os

# READING REQUIREMENTS FROM FILE
required = [
    "Brotli==1.1.0",
    "certifi==2024.2.2",
    "charset-normalizer==3.3.2",
    "click==8.1.3",
    "cryptography==42.0.2",
    "idna==3.6",
    "importlib-metadata==7.0.1",
    "joblib==1.3.2",
    "Levenshtein==0.25.0",
    "mutagen==1.47.0",
    "platformdirs==4.2.0",
    "pycryptodomex==3.20.0",
    "pyperclip==1.8.2",
    "python-Levenshtein==0.25.0",
    "rapidfuzz==3.6.1",
    "regex==2023.12.25",
    "requests>=2.32.2",
    "textblob==0.18.0.post0",
    "tomli==2.0.1",
    "tqdm==4.66.2",
    "urllib3==2.2.1",
    "websockets==13.0.1",
    "yapf==0.40.2",
    "yt-dlp>=2024.3.10",
    "zipp==3.17.0",
    "translate==3.6.1",
    "langdetect==1.0.9",
    "deep-translator==1.11.4",
    "netifaces>=0.11.0",
    "speedtest-cli>=2.1.3",
    "psutil>=5.9.0",
    "setuptools>=40.8.0",
]

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
