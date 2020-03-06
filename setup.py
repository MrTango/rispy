from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path
import re

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


def get_version():
    regex = r"""^__version__ = "(.*)"$"""
    with open("rispy/__init__.py", "r") as f:
        text = f.read()
    return re.findall(regex, text, re.MULTILINE)[0]


setup(
    name="rispy",
    version=get_version(),
    description="Reads RIS files into dictionaries via a generator for large files",
    long_description=long_description,
    url="https://github.com/mrtango/RISparser",
    author="Maik Derstappen (MrTango)",
    author_email="md@derico.de",
    license="GNU General Public License v2 (GPLv2)",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="RIS parser bibliograph",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[],
    extras_require={
        "dev": ["black==19.10b0", "flake8==3.7.9", "check-manifest", "wheel"],
        "test": ["coverage", "pytest"],
    },
)
