from setuptools import find_packages
from setuptools import setup


def get_install_requires():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines() if not line.startswith("-")]


setup(
    name="gdslib",
    version="0.1.3",
    url="https://github.com/gdsfactory/gdslib",
    license="MIT",
    author="Joaquin",
    description="gdslibrary library of compact models and GDS metadata",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
)
