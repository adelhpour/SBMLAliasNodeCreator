from setuptools import setup
from setuptools import find_packages

MAJOR = 0
MINOR = 0
MICRO = 2

version = f'{MAJOR}.{MINOR}.{MICRO}'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sbmlaliasnodecreator",
    version=version,
    author="Adel Heydarabadipour",
    author_email="adelhp@uw.edu",
    description="Create alias nodes for heavily connected nodes in an SBML model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adelhpour/SBMLAliasNodeCreator",
    project_urls={
        "Bug Tracker": "https://github.com/adelhpour/SBMLAliasNodeCreator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["os", "libsbml", "SBMLDiagrams==1.3.2"],
    scripts=["testcases/example1.py", "testcases/example2.py"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8"
)
