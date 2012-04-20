TORmeter by Skygge @ Bloodworthy EU
contact at oldschoolguild.enjin.com


Installing and running:


Simply copy/extract the TORmeter folder into your 

/Users/.../My Documents/Star Wars - The Old Republic/CombatLogs

Run the .exe to start the program.



Loading files:

Either manually load a spesific file throught the "file->Open log" menu, 
or simply check "load latest file" in the File menu. It will not load empty files.


"Min Enc. time:" sets the threshold for which you want to ignore short encounters.
"Enc. separation threshold:" sets the threshold for which you want to merge two close fights as one, i.e. using combat drop abilities in-fight.


Analyzing files:

After opening a file, or selecting to open the latest, choose an encounter from the menu. It will display the 10 latest fights. Set thresholds to ignore unimportant ones.

"Analyze:" Calculates values and displays them in a pop-up window.
"Write to file:" Writes ALL info from the log in a new file located in your TORmeter folder with the name of the input log + a "_out" suffix. It should automatically open.
"Plot DPS:" Shows your average dps on all times throughout the encounter.
"Plot HPS:" Same as above for HPS.


Known issues:

-You have to reopen or re-check logs/options if you change the "Min Enc time" or separation threshold values before they take effect.
-The Bioware logs does not allways display an Exit Combat if you i.e. loose a duel or die in odd ways. In that case TORmeter will make an "educated guess" of your end time.
-The Bioware logs are not dumped to in real-time, so encounters might not appear in their whole before a while.

Companions:
Companion healing and damage are counted as your own. An option to separate this will be implemented if the need arise.


About:
TORmeter is coded in Python using Tkinter GUI and matplotlib plot tools.