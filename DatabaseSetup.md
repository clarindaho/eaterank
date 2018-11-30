## EECS 341 Project
Clarinda Ho (cqh), Seohyun Jung (sxj393), Jason Shin (jjs270), Catherine Tsuei (cwt26)

### Database Setup

#### Manual Setup
1. Install *Virtual Environment*
	- ***sudo apt-get install virtualenv***
	- Enter **sudo** password if prompted
2. **cd** to project directory **eaterank**
3. Create new virtual environment named **eaterank**
	<br> ***virtualenv eaterank -p python3***
4. Activate the virtual environment
	- ***cd eaterank***
	- ***source bin/activate***
5. Install *Flask* on the virtual environment
	<br> ***pip3 install flask***
6. Install *MySQL Connector* on the virtual environment
	<br> ***pip3 install mysql-connector***
7. Install supporting libraries on the virtual environment
	- ***pip3 install requests***
	- ***pip3 install logger***
	- ***pip3 install configparser***
	- ***pip3 install bs4***
8. Create database on localhost
	- ***cd ../***
	- ***sudo mysql -u root -p -e "SOURCE setup.sql;"***
	- Enter MySQL password for **'root'**
9. To deactivate the virtual environment
	<br> ***deactivate***

#### Automatic Setup
1. **cd** to project directory **eaterank**
2. Make shell script executable
	<br> ***chmod +x setup.sh*** or ***chmod 755 setup.sh***
3. Run the shell script executable
	- ***sudo ./setup.sh***
	- Enter **sudo** password if prompted
4. Enter MySQL password for **'root'** when prompted

### Potential Error Solutions
- **'no module named configparser'**
	- ***pip3 install configparser***
- **'caching sha_2_password cannot be loaded'**
	- If using MySQL on Windows, set the user authentication method to **standard**