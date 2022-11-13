# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="finances",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    version="0.1.0",
    description="Net worth calculation package",
    author="Sergei Issaev",
)
