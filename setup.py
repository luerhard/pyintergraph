import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyintergraph", 
    version="1.0",
    author="Lukas Erhard",
    author_email="luerhard@googlemail.com",
    description=("Exchange Python-Graph-Objects between networkx, igraph and graph-tools"),
    license="MIT",
    url="https://gitlab.com/luerhard/pyintergraph/-/archive/v1.0/pyintergraph-v1.0.tar.gz",
    keywords="networkx python-igraph igraph graph_tool intergraph convert graph network",
    packages=find_packages(),
    long_description=read("README.md"),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities"
    ],
)
