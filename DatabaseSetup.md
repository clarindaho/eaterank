## EECS 341 Project
Clarinda Ho (cqh), Seohyun Jung (sxj393), Jason Shin (jjs270), Catherine Tsuei (cwt26)

### Database Setup

#### Manual Setup
1. Install *Virtual Environment* by running
	- ***sudo apt-get install virtualenv***
	- Enter **sudo** password if prompted
2. Create new virtual environment named **eaterank**
	<br> ***virtualenv eaterank***
3. Activate the virtual environment
	- ***cd eaterank***
	- ***source bin/activate***
4. Install *Flask* on the virtual environment
	<br> ***pip3 install flask***
5. Install *MySQL Connector* on the virtual environment
	<br> ***pip3 install mysql-connector***
6. Install supporting libraries on the virtual environment
	- ***pip3 install requests***
	- ***pip3 install logger***
	- ***pip3 install configparser***
	- ***pip3 install bs4***
7. Create database on localhost
	- ***mysql -u root -p***
	- Enter MySQL password for **'root'**
	- ***SOURCE setup.sql;***
	- ***quit;***
8. To deactivate the virtual environment
	<br> ***deactivate***

#### Automatic Setup
1. Make shell script executable
	<br> ***chmod +x setup.sh***
2. Run the shell script executable
	<br> ***./setup.sh***
3. Enter **sudo** password if prompted
4. Enter MySQL password for **'root'** when prompted

### Potential Error Solutions
- **'no module named configparser'**
	- ***pip3 install configparser***
- **'caching sha_2_password cannot be loaded'**
	- If using MySQL on Windows, set the user authentication method to **standard**