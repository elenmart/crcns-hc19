#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import sys
from setuptools import setup

if sys.hexversion < 0x02070000:
    raise RuntimeError("Python 2.7 or higher required")

# Replace all instances of `comp-neurosci-skeleton` with the name of your project
setup(
    name="comp-neurosci-crcns-hc19",
    version="0.0.1",
    package_dir={'comp-neurosci-crcns-hc19': 'src'},
    packages=["comp-neurosci-crcns-hc19"],

    description="",
    long_description="",
    install_requires=[
        "numpy==1.16.0",
        "scipy==1.2.0",
        "pandas==0.24.1",
        "matplotlib==2.2.2",
        "seaborn==0.9.0",
        "notebook==5.7.6",
    ],

    author="Christof Fehrman",
    maintainer='Christof Fehrman',
)
