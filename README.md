## EECS 341 Project
Clarinda Ho (cqh), Seohyun Jung (sxj393), Jason Shin (jjs270), Catherine Tsuei (cwt26)

### Requirements
- Python 3
- mySQL
- **sudo** privileges

### Setting Up the Database
See *DatabaseSetup.md*.

### Hosting the Web Application
1. Setup host configurations
	- cd to project directory **eaterank**
	- Edit file ***config.ini*** and replace the value specified in **host** under section **[app]** with the desired host's IP address. The IP address can be left as is if testing only internally on the localhost.
	- **Optional**: edit file ***config.ini*** and replace the value specified in **port** under section **[app]** with the desired port
2. Start hosting the web application
	- cd to project directory **eaterank**
	- ***python3 routes.py***
3. Testing the web application
	- Open the URL listed in a browser for as many tabs as users in the group
	- Have one tab instance be the group leader and the others as regular users

### Group Leader
1. Click **Create a Group**
2. Enter ZIP code of where you want to search for restaurants. Press **Enter** after you finish typing in the ZIP code.
3. Select the desired cuisines from the displayed list. Click **Submit** after you finish selecting all desired cuisines.
4. The group code will appear on the page. Share this group code with your other users. Click **Enter Waiting Room** to wait for others to join using the group code.
	- The group code may take a while to appear. This is because behind the scenes, we are looking up all the restaurants' information and pictures.
5. A waiting page will be displayed. Once all users have entered the group code on their end, click **Start Voting** to begin the voting process.
5. See *Voting* section

### Regular User
1. Click **Join an Existing Group**
2. Enter the group code (given by the group leader) in the text box provided. Press **Enter** after you finish typing in the group code.
	- If valid group code, proceed to *Step 3*
	- If invalid group code, an error message will be displayed
	- If voting has already started for that group, an error message will be displayed
3. Wait for group leader to begin the voting process. Once the voting process has begun, voting page will be automatically displayed.
4. See *Voting* section

### Voting
1. Restaurant information will be displayed with buttons for approving/disapproving
2. Click on desired button. The next restaurant to vote on will appear automatically.
3. Repeat *Steps 1* and *2* for remaining restaurants (there will be 10 restaurants in total)
4. After voting on the last restaurant
	- If group leader, wait for all group members to finish voting before clicking **Display Results**
	- If regular user, wait for the group leader to display the final restaurant result
5. Final result will be displayed with the restaurant that has the most popular votes