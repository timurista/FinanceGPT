#!/bin/bash

# Check if the user has provided a directory
if [ -z "$1" ]; then
    echo "Error: Please provide a directory."
    exit 1
fi

# Set the provided directory as the working directory
DIRECTORY="$1"
cd "$DIRECTORY" || exit

# Source the virtual environment
source venv/bin/activate

# Call the main.py file
python main.py

# Deactivate the virtual environment
deactivate