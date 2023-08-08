"""
Author: Shailesh Appukuttan
Date: 07/08/2023
"""
from setuptools import setup, find_packages

setup(
    name="sckan-compare",
    version="0.0.6",
    description="A package for retrieving and visualizing data contained in     SCKAN (e.g., across species, relationship to spinal segments) to highlight similarities and differences in neuronal pathways",
    author="Shailesh Appukuttan, Hiba Ben Aribi, Pranjal Garg, Gautam Kumar",
    author_email="appukuttan.shailesh@gmail.com",
    license="Apache-2.0",
    package_data={'': ['data/*.*']},
    packages=find_packages(),
)
