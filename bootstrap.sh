#!/usr/bin/env bash

set -e

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
