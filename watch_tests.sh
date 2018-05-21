#!/usr/bin/env bash

cd src
find . -name '*.py' | entr python -m unittest -v
