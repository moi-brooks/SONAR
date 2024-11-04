#!/bin/bash

# Update system packages
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential curl wget

# Install Miniconda if not already installed
if ! command -v conda &> /dev/null; then
    echo "Installing Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
    rm miniconda.sh
    
    # Initialize conda
    eval "$($HOME/miniconda/bin/conda shell.bash hook)"
    conda init
    
    # Reload shell to apply conda changes
    exec $SHELL
fi

# Create conda environment from yml file
echo "Creating conda environment..."
conda env create -f conda/environment.yml

# Activate environment
echo "Activating environment..."
conda activate phishing_env

# Install spacy language model
echo "Installing spaCy language model..."
python -m spacy download en_core_web_lg

# Install NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Set up pre-commit hooks
echo "Setting up pre-commit..."
pip install pre-commit
pre-commit install

echo "Setup complete! 🚀"
echo "To activate the environment, run: conda activate phishing_env"