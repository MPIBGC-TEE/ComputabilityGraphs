#!/bin/bash
set -e
conda install -y -c conda-forge --file requirements.conda
pip install -e .
