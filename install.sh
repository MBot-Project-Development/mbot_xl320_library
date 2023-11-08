#!/bin/bash

# Get the current working directory (where the script is run from)
WORKSPACE_PATH=$(pwd)

# Ensure that the Dynamixel SDK submodule is initialized and updated
echo "Initializing and updating submodules..."
git submodule init
git submodule update

# Install Dynamixel SDK from the submodule
echo "Installing Dynamixel SDK..."
cd "$WORKSPACE_PATH/mbot_xl320_library/DynamixelSDK/python"
sudo python3 setup.py install || { echo 'Installing Dynamixel SDK failed.'; exit 1; }

# Install mbot_xl320_library
echo "Installing mbot_xl320_library..."
cd "$WORKSPACE_PATH/mbot_xl320_library"
sudo python3 setup.py install || { echo 'Installing mbot_xl320_library failed.'; exit 1; }

echo "Installation completed successfully."
