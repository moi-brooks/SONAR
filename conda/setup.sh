#!/bin/bash

# Update WSL and install system dependencies
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential curl wget

# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
rm miniconda.sh

# Initialize conda
eval "$($HOME/miniconda/bin/conda shell.bash hook)"
conda init

# Create and activate environment
conda env create -f environment.yml
conda activate phishing_env

# Install spacy language model
python -m spacy download en_core_web_lg

# Set up pre-commit hooks
pip install pre-commit
pre-commit install
