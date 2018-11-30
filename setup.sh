!/bin/sh

# Install virtual environment by running
sudo apt-get install virtualenv

# Create virtual environment named eaterank
virtualenv eaterank

# Activate virtual environment
cd eaterank
source bin/activate

# Install flask on virtual environment
pip3 install flask

# Install mysql connector
pip3 install mysql-connector

# Install supporting libraries
pip3 install requests
pip3 install logger
pip3 install configparser
pip3 install bs4

# Create database on local machine
cd ../
mysql -u root -p -e "SOURCE setup.sql;"