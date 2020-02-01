#!/bin/bash

# костыль
export PYTHONPATH="${PYTHONPATH}:vlf"

# Deprecation ignore because something inside pymunk screaming
# Ignored for better test during development >_<
python -m pytest -W ignore::DeprecationWarning
