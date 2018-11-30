## EECS 341 Project
Clarinda Ho (cqh), Seohyun Jung (sxj393), Jason Shin (jjs270), Catherine Tsuei (cwt26)

### Database Setup
1. Install virtual environment by running
<br>sudo apt-get install virtualenv

2. Create virtual environment named eaterank
virtualenv eaterank

3. Activate virtual environment
cd eaterank
source bin/activate

4. Install flask on virtual environment
pip install flask

5. Install mysql connector
pip install mysql-connector

6. Install supporting libraries
pip install requests
pip install logger
pip install configparser

7. Create database on local machine
mysql -u root -p
source setup.sql;
quit;

8. To deactivate virtual environment
deactivate

*** Potential error solutions ***
'no module named configparser':
pip install configparser

'caching sha_2_password cannot be loaded':
if using MySQL on Windows, set the user authentication method to standard
*********************************