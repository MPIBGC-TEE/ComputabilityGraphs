#!/bin/bash
set -e
conda install -y -c conda-forge --file requirements.conda
python setup.py develop
