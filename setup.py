import os
import importlib.util
from setuptools import setup, find_packages  # pyright: ignore[reportMissingModuleSource]

def _load_module_from_path(module_name, *path_parts):
    module_path = os.path.join(os.path.dirname(__file__), *path_parts)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# READING README.MD FOR LONG DESCRIPTION
with open("README.md", "r", encoding="utf-8") as fh: long_description = fh.read()

# LOADING REQUIREMENTS
requirements_module = _load_module_from_path("requirements", "autotools", "utils", "requirements.py")
read_requirements = requirements_module.read_requirements
tool_registry_module = _load_module_from_path("tool_registry", "autotools", "tool_registry.py")

required = read_requirements("requirements.txt")
dev_required = read_requirements("requirements-dev.txt")

# SETUP CONFIGURATION FOR PACKAGE DISTRIBUTION
setup(
    name='Open-AutoTools',
    version='0.0.7rc1',
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=required,
    extras_require={"dev": dev_required, "test": dev_required},
    
    # ENTRY POINTS FOR CLI COMMANDS
    entry_points={
        "console_scripts": list(tool_registry_module.CONSOLE_SCRIPT_ENTRY_POINTS),
    },
    
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
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
