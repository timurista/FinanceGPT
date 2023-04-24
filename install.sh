#!/bin/bash

# Check if the user has provided a directory
if [ -z "$1" ]; then
    echo "Error: Please provide a directory."
    exit 1
fi

# Set the provided directory as the working directory
DIRECTORY="$1"
cd "$DIRECTORY" || exit

# Create a virtual environment with Python 3.10
python3.10 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
