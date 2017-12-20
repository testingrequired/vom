#!/usr/bin/env bash

set -e

python -m pytest
python setup.py bdist_wheel --universal