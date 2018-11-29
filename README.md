## EECS 341 Project
Clarinda Ho (cqh), Seohyun Jung (sxj393), Jason Shin (jjs270), Catherine Tsuei (cwt26)

Setting up the database:
See DatabaseSetup.

1. Run the website
   cd to project directory 'eaterank'
   python routes.py
2. Open the URL listed in a browser in as many tabs as users in the group.
   Have one tab instance be the group leader and the others regular users.

Group Leader
1. Click 'Create a Group'.
2. Enter zipcode of where you want to search for restaurants.
   Share the group code listed on this page with your other users.
   Click Submit.
3. Select the desired cuisines from the displayed list and click Submit.
4. A waiting page will be displayed. Once all users have entered the group code on their ends,
   click Start Voting.
5. See Voting section.

Regular User
1. Click 'Join an Existing Group'.
2. Enter the group code in textbox provided. Click Submit.
   a. if valid code, will proceed to 3.
   b. if invalid code, error message will be displayed.
   c. if voting has already started for that group, error message will be displayed.
3. Wait for group leader to begin the voting process. Will be taken to the voting page.
4. See Voting section.

Voting
1. Restaurant information will be displayed with buttons for approving/disapproving.
2. Click on desired button. Will be taken to the next restaurant to vote on.
3. Continue for remaining restaurants (there will be 10 in total);
4. After voting on the last restaurant:
   a. if group leader, wait for all user to finish voting before clicking 'Display results'
   b. if regular user, wait for group leader to display the final restaurant result
5. Final result will be displayed with the restaurant that has the most popular votes.