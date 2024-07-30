import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="picogrid-pytest-split-tests",
    description=(
        "A Picogrid Fork of Pytest plugin for running a subset of your tests by "
        "splitting them in to equally sized groups. Forked from "
        "Mark Adams' original project pytest-test-groups."
    ),
    url="https://github.com/picogrid/pytest-split-tests",
    author="Picogrid",
    author_email="software@picogrid.com",
    packages=["pytest_split_tests"],
    version="2.0.0",
    long_description=read("README.rst"),
    install_requires=["pytest>=2.5"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "pytest11": [
            "split-tests = pytest_split_tests",
        ]
    },
)
