from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="Australian-Rain-Weather-Prediction",
    version="0.1",
    author="Chinmay",
    packages=find_packages(),
    install_requires = requirements,
)