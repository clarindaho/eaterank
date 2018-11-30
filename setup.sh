!/bin/sh

# Install virtual environment by running
sudo apt-get install virtualenv

# Create virtual environment named eaterank
virtualenv eaterank

# Activate virtual environment
cd eaterank
source bin/activate

# Install flask on virtual environment
pip install flask

# Install mysql connector
pip install mysql-connector

# Install supporting libraries
pip install requests
pip install logger
pip install configparser

# Create database on local machine
cd ../
mysql -u root -p -e "SOURCE setup.sql;"