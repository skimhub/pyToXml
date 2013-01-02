import os
from setuptools import setup


# Utility function to read the README file.  Used for the
# long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to
# put a raw string in below ...
#
# despite the manifest the readme.md will be missing when installed
# from pypi, so we need to just fail silently here.
def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return ""

setup(
    name="pyToXml",
    version="1.0.0",
    author="Skimlinks",
    author_email="dev@skimlinks.com",
    description=("Simple Python to XML library."),
    keywords="python skimlinks xml dict array",
    url="https://github.com/skimhub/pyToXml.git",
    packages=["pytoxml"],
    long_description=read('README.md'),
    install_requires=[
        "lxml==3.0.2",
        "six",
    ]
)
