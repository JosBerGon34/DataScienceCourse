#!/usr/bin/env bash

jupyter kernelspec uninstall ds-core -f

rm -rf .venv-core

echo
echo "Workspace removed."
