#!/usr/bin/env bash

set -e

python -m pytest
python setup.py sdist bdist_wheel

