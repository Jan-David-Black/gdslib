from setuptools import find_packages
from setuptools import setup


def get_install_requires():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines() if not line.startswith("-")]


setup(
    name="gdslib",
    version="0.3.1",
    url="https://github.com/gdsfactory/gdslib",
    license="MIT",
    author="gdslib community",
    description="library of component models",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
)
