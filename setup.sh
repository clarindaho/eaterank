#!/bin/bash

# Install Virtual Environment
sudo apt-get install virtualenv

# Create new virtual environment named eaterank
virtualenv eaterank -p python3

# Activate the virtual environment
cd eaterank
source bin/activate

# Install Flask on the virtual environment
pip3 install flask

# Install MySQL Connector
pip3 install mysql-connector

# Install supporting libraries
pip3 install requests
pip3 install logger
pip3 install configparser
pip3 install bs4

# Create database on localhost
cd ../
sudo mysql -u root -p -e "SOURCE setup.sql;"