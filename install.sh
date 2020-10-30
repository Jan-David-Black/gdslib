#!/bin/sh

pip install -r requirements_dev.txt --upgrade
pip install -r requirements.txt --upgrade
pip install -e .
pre-commit install
