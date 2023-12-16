#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt-get update

# Install graphviz
echo "Installing Graphviz..."
sudo apt-get install graphviz -y

# Install Python packages using pip
echo "Installing pandas and graphviz for Python..."
pip install pandas
pip install graphviz

echo "Installation completed!"
