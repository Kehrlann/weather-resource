#!/usr/bin/env bash

source venv/bin/activate
cd src
find . -name '*.py' | entr python -m unittest -v
