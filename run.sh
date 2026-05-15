#!/usr/bin/env bash
set -euo pipefail

VENV=.venv
PYTHON=$VENV/bin/python

if [ ! -f "$PYTHON" ]; then
  echo "Virtualenv not found — creating $VENV..."
  python3 -m venv $VENV
fi

echo "Installing/ upgrading pip and requirements from Docs/requirements.txt..."
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -r documentacion/requirements.txt

echo "Starting application (Flask)..."
$PYTHON main.py
